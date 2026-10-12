import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from services.models import ServiceProvider


class Command(BaseCommand):
    help = "Import marketplace users and service providers from JSON files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            default="users.json",
            help="Path to exported users JSON file",
        )
        parser.add_argument(
            "--providers",
            default="providers.json",
            help="Path to exported providers JSON file",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        users_path = Path(options["users"])
        providers_path = Path(options["providers"])

        if not users_path.is_file() or not providers_path.is_file():
            raise CommandError(
                "Both users.json and providers.json must be available."
            )

        with users_path.open(encoding="utf-8") as file:
            users_data = json.load(file)

        with providers_path.open(encoding="utf-8") as file:
            providers_data = json.load(file)

        if not isinstance(users_data, list) or not isinstance(
            providers_data, list
        ):
            raise CommandError("The JSON files must contain lists of records.")

        imported_users = 0
        skipped_users = 0

        for item in users_data:
            if item.get("model", "").lower() != "auth.user":
                continue

            fields = item["fields"]
            username = fields["username"]

            if User.objects.filter(username=username).exists():
                skipped_users += 1
                continue

            User.objects.create(
                id=item.get("pk"),
                **fields,
            )
            imported_users += 1

        imported_providers = 0
        skipped_providers = 0

        for item in providers_data:
            if item.get("model", "").lower() != "services.serviceprovider":
                continue

            fields = item["fields"]
            user_id = fields.get("user")

            if not User.objects.filter(pk=user_id).exists():
                self.stderr.write(
                    f"Skipped provider record {item.get('pk')}: "
                    f"user ID {user_id} is missing."
                )
                skipped_providers += 1
                continue

            if ServiceProvider.objects.filter(user_id=user_id).exists():
                skipped_providers += 1
                continue

            ServiceProvider.objects.create(
                id=item.get("pk"),
                **fields,
            )
            imported_providers += 1

        self.stdout.write(self.style.SUCCESS("Import completed."))
        self.stdout.write(f"Users imported: {imported_users}")
        self.stdout.write(f"Users skipped: {skipped_users}")
        self.stdout.write(f"Providers imported: {imported_providers}")
        self.stdout.write(f"Providers skipped: {skipped_providers}")