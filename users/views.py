from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from services.models import ServiceProvider
from .models import CustomerProfile


def register(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            error = "Passwords do not match."

        elif not username:
            error = "Please enter a username."

        elif not email:
            error = "Please enter an email."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        elif User.objects.filter(email__iexact=email).exists():
            error = "Email already exists."

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            profile = CustomerProfile.objects.get(user=user)
            profile.phone = phone
            profile.save()

            login(request, user)

            return redirect("home")

    return render(
        request,
        "register.html",
        {
            "error": error
        }
    )


def provider_register(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        category = request.POST.get("category")
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price")
        working_hours = request.POST.get("working_hours", "").strip()
        image = request.POST.get("image", "").strip()

        if password != confirm_password:
            error = "Passwords do not match."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        elif User.objects.filter(email__iexact=email).exists():
            error = "Email already exists."

        elif not category:
            error = "Please select a service category."

        elif not description:
            error = "Please enter your service description."

        elif not price:
            error = "Please enter your starting price."

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            ServiceProvider.objects.create(
                user=user,
                phone=phone,
                category=category,
                location=location,
                description=description,
                price=price,
                working_hours=working_hours,
                image=image
            )

            login(request, user)

            return redirect("provider_profile")

    return render(
        request,
        "provider_register.html",
        {
            "error": error,
            "categories": ServiceProvider.CATEGORY_CHOICES
        }
    )


def customer_login(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user_by_email = User.objects.filter(
            email__iexact=email
        ).first()

        if user_by_email:

            user = authenticate(
                request=request,
                username=user_by_email.username,
                password=password
            )

            if user is not None:

                provider = ServiceProvider.objects.filter(
                    user=user
                ).first()

                if provider:

                    error = (
                        "This is a provider account. "
                        "Please use Provider Login."
                    )

                else:

                    login(request, user)

                    return redirect("home")

            else:

                error = "Invalid email or password."

        else:

            error = "Invalid email or password."

    return render(
        request,
        "customer_login.html",
        {
            "error": error
        }
    )


def provider_login(request):
    error = None

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user_by_email = User.objects.filter(
            email__iexact=email
        ).first()

        if user_by_email:

            user = authenticate(
                request=request,
                username=user_by_email.username,
                password=password
            )

            if user is not None:

                provider = ServiceProvider.objects.filter(
                    user=user
                ).first()

                if provider:

                    login(request, user)

                    return redirect(
                        "provider_dashboard"
                    )

                else:

                    error = (
                        "This account is not registered "
                        "as a service provider."
                    )

            else:

                error = "Invalid email or password."

        else:

            error = "Invalid email or password."

    return render(
        request,
        "provider_login.html",
        {
            "error": error
        }
    )


@login_required
def customer_profile(request):

    provider = ServiceProvider.objects.filter(
        user=request.user
    ).first()

    if provider:
        return redirect("provider_dashboard")

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    error = None
    success = None

    if request.method == "POST":

        action = request.POST.get("action", "profile")

        # ==================================================
        # CHANGE PASSWORD
        # ==================================================

        if action == "change_password":

            current_password = request.POST.get(
                "current_password",
                ""
            )

            new_password = request.POST.get(
                "new_password",
                ""
            )

            confirm_new_password = request.POST.get(
                "confirm_new_password",
                ""
            )

            if not current_password:

                error = "Please enter your current password."

            elif not request.user.check_password(
                current_password
            ):

                error = "Current password is incorrect."

            elif not new_password:

                error = "Please enter a new password."

            elif new_password != confirm_new_password:

                error = "New passwords do not match."

            elif current_password == new_password:

                error = (
                    "New password must be different "
                    "from your current password."
                )

            else:

                try:

                    validate_password(
                        new_password,
                        request.user
                    )

                    request.user.set_password(
                        new_password
                    )

                    request.user.save()

                    # Keep the user logged in after changing
                    # the password.
                    update_session_auth_hash(
                        request,
                        request.user
                    )

                    success = (
                        "Password changed successfully."
                    )

                except ValidationError as validation_error:

                    error = " ".join(
                        validation_error.messages
                    )

        # ==================================================
        # EDIT PROFILE
        # ==================================================

        else:

            username = request.POST.get(
                "username",
                ""
            ).strip()

            email = request.POST.get(
                "email",
                ""
            ).strip()

            phone = request.POST.get(
                "phone",
                ""
            ).strip()

            if not username:

                error = "Username cannot be empty."

            elif User.objects.filter(
                username=username
            ).exclude(
                id=request.user.id
            ).exists():

                error = "Username already exists."

            elif not email:

                error = "Email cannot be empty."

            elif User.objects.filter(
                email__iexact=email
            ).exclude(
                id=request.user.id
            ).exists():

                error = "Email already exists."

            else:

                request.user.username = username
                request.user.email = email
                request.user.save()

                profile.phone = phone
                profile.save()

                success = (
                    "Profile updated successfully."
                )

    from bookings.models import Booking

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by(
        "-created_at"
    )

    total_bookings = bookings.count()

    completed_bookings = bookings.filter(
        status="Completed"
    ).count()

    pending_bookings = bookings.filter(
        status="Pending"
    ).count()

    accepted_bookings = bookings.filter(
        status="Accepted"
    ).count()

    recent_bookings = bookings[:5]

    return render(
        request,
        "customer_profile.html",
        {
            "profile": profile,
            "bookings": bookings,
            "recent_bookings": recent_bookings,
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "pending_bookings": pending_bookings,
            "accepted_bookings": accepted_bookings,
            "error": error,
            "success": success
        }
    )


@login_required
def user_logout(request):

    logout(request)

    return redirect("home")