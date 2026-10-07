from django.contrib import admin
from django.urls import path

from services.views import (
    home,
    provider_profile,
    service_list
)

from bookings.views import (
    book_service,
    provider_dashboard,
    update_booking_status,
    cancel_booking,
    my_bookings,
    add_review,
    provider_reviews,
    provider_detail,
    payment_page,
    payment_success
)

from users.views import (
    register,
    provider_register,
    customer_login,
    provider_login,
    customer_profile,
    user_logout
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "provider-register/",
        provider_register,
        name="provider_register"
    ),

    path(
        "customer-login/",
        customer_login,
        name="customer_login"
    ),

    path(
        "provider-login/",
        provider_login,
        name="provider_login"
    ),

    path(
        "logout/",
        user_logout,
        name="logout"
    ),

    path(
        "provider-profile/",
        provider_profile,
        name="provider_profile"
    ),

    path(
        "services/",
        service_list,
        name="service_list"
    ),

    path(
        "provider/<int:provider_id>/",
        provider_detail,
        name="provider_detail"
    ),

    path(
        "book/<int:provider_id>/",
        book_service,
        name="book_service"
    ),

    path(
        "provider-dashboard/",
        provider_dashboard,
        name="provider_dashboard"
    ),

    path(
        "update-booking-status/<int:booking_id>/<str:status>/",
        update_booking_status,
        name="update_booking_status"
    ),

    path(
        "cancel-booking/<int:booking_id>/",
        cancel_booking,
        name="cancel_booking"
    ),

    path(
        "my-bookings/",
        my_bookings,
        name="my_bookings"
    ),

    path(
        "add-review/<int:provider_id>/",
        add_review,
        name="add_review"
    ),

    path(
        "provider-reviews/<int:provider_id>/",
        provider_reviews,
        name="provider_reviews"
    ),

    path(
        "customer-profile/",
        customer_profile,
        name="customer_profile"
    ),

    path(
        "payment/<int:booking_id>/",
        payment_page,
        name="payment_page"
    ),

    path(
        "payment-success/<int:booking_id>/",
        payment_success,
        name="payment_success"
    ),
]