from django.contrib import admin
from .models import ServiceProvider


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'category',
        'location',
        'price',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'user__first_name',
        'user__email',
        'phone',
        'location',
    )
# Register your models here.
