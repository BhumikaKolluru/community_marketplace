from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2

from .models import ServiceProvider
from bookings.models import Review


def home(request):
    return render(
        request,
        "home.html"
    )


@login_required
def provider_profile(request):

    # Only registered service providers can access this page
    provider = ServiceProvider.objects.filter(
        user=request.user
    ).first()

    if provider is None:
        return redirect("home")

    if request.method == "POST":

        phone = request.POST.get("phone")
        category = request.POST.get("category")
        location = request.POST.get("location")
        description = request.POST.get("description")
        price = request.POST.get("price")
        working_hours = request.POST.get("working_hours")
        image = request.POST.get("image")

        if not price:
            price = 0

        provider.phone = phone
        provider.category = category
        provider.location = location
        provider.description = description
        provider.price = price
        provider.working_hours = working_hours
        provider.image = image

        provider.save()

        return redirect("home")

    return render(
        request,
        "provider_profile.html",
        {
            "provider": provider
        }
    )


LOCATION_COORDINATES = {
    "vijayawada": (16.5062, 80.6480),
    "gudivada": (16.4350, 80.9900),
    "machilipatnam": (16.1875, 81.1389),
    "chirala": (15.8246, 80.3521),
    "guntur": (16.3067, 80.4365),
    "tenali": (16.2428, 80.6400),
    "eluru": (16.7107, 81.0952),
    "ongole": (15.5057, 80.0499),
    "hyderabad": (17.3850, 78.4867),
    "kadapa": (14.4673, 78.8242),
    "tirupati": (13.6288, 79.4192),
    "nellore": (14.4426, 79.9865),
    "visakhapatnam": (17.6868, 83.2185),
    "kakinada": (16.9891, 82.2475),
    "rajahmundry": (17.0005, 81.8040),
}


def calculate_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):

    earth_radius = 6371

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    difference_latitude = radians(
        latitude2 - latitude1
    )

    difference_longitude = radians(
        longitude2 - longitude1
    )

    a = (
        sin(difference_latitude / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(difference_longitude / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def service_list(request):

    providers = ServiceProvider.objects.all()

    category = request.GET.get("category")

    if category:
        providers = providers.filter(
            category=category
        )

    search = request.GET.get("search")

    if search:
        providers = providers.filter(
            Q(user__first_name__icontains=search)
            |
            Q(user__username__icontains=search)
            |
            Q(category__icontains=search)
            |
            Q(location__icontains=search)
            |
            Q(description__icontains=search)
        )

    location = request.GET.get("location")

    selected_location = None

    if location:

        location_key = location.strip().lower()

        if location_key in LOCATION_COORDINATES:

            selected_location = location.strip()

            providers = providers.filter(
                location__iexact=selected_location
            )

            customer_latitude, customer_longitude = (
                LOCATION_COORDINATES[location_key]
            )

            nearby_providers = []

            for provider in providers:

                if (
                    provider.latitude is not None
                    and provider.longitude is not None
                ):

                    distance = calculate_distance(
                        customer_latitude,
                        customer_longitude,
                        provider.latitude,
                        provider.longitude
                    )

                    provider.distance = round(
                        distance,
                        1
                    )

                else:
                    provider.distance = 0

                nearby_providers.append(
                    provider
                )

            nearby_providers.sort(
                key=lambda provider:
                provider.distance
            )

            providers = nearby_providers

    for provider in providers:

        reviews = Review.objects.filter(
            provider=provider
        )

        review_count = reviews.count()

        if review_count > 0:

            total_rating = sum(
                review.rating
                for review in reviews
            )

            average_rating = round(
                total_rating / review_count,
                1
            )

        else:
            average_rating = 0

        provider.average_rating = average_rating
        provider.review_count = review_count

    return render(
        request,
        "services.html",
        {
            "providers": providers,
            "selected_location": selected_location,
            "location_search": location,
        }
    )


def provider_detail(request, provider_id):

    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id
    )

    reviews = Review.objects.filter(
        provider=provider
    ).order_by("-created_at")

    if reviews.exists():

        total_rating = sum(
            review.rating
            for review in reviews
        )

        average_rating = round(
            total_rating / reviews.count(),
            1
        )

    else:

        average_rating = 0

    return render(
        request,
        "provider_detail.html",
        {
            "provider": provider,
            "reviews": reviews,
            "average_rating": average_rating,
            "review_count": reviews.count()
        }
    )