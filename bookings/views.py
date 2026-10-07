from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Booking, Review, Payment
from services.models import ServiceProvider
from users.models import CustomerProfile


@login_required
def book_service(request, provider_id):

    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id
    )

    error = None

    if request.method == "POST":

        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        address = request.POST.get("address")
        message = request.POST.get("message")

        if not booking_date:
            error = "Please select a booking date."

        elif booking_date < str(timezone.localdate()):
            error = "You cannot book a service for a past date."

        elif not booking_time:
            error = "Please select a booking time."

        elif not address or not address.strip():
            error = "Please enter your service address."

        else:

            existing_booking = Booking.objects.filter(
                provider=provider,
                booking_date=booking_date,
                booking_time=booking_time,
                status__in=[
                    "Pending",
                    "Accepted"
                ]
            ).exists()

            if existing_booking:
                error = (
                    "This provider is already booked "
                    "at the selected date and time."
                )

            else:

                booking = Booking.objects.create(
                    customer=request.user,
                    provider=provider,
                    booking_date=booking_date,
                    booking_time=booking_time,
                    address=address.strip(),
                    message=message,
                    status="Pending"
                )

                Payment.objects.create(
                    booking=booking,
                    customer=request.user,
                    amount=provider.price,
                    payment_status="Pending"
                )

                return redirect("my_bookings")

    return render(
        request,
        "booking.html",
        {
            "provider": provider,
            "error": error
        }
    )


@login_required
def provider_dashboard(request):

    provider = ServiceProvider.objects.filter(
        user=request.user
    ).first()

    if provider is None:
        return redirect("home")

    all_bookings = Booking.objects.filter(
        provider=provider
    )

    pending_count = all_bookings.filter(
        status="Pending"
    ).count()

    accepted_count = all_bookings.filter(
        status="Accepted"
    ).count()

    completed_count = all_bookings.filter(
        status="Completed"
    ).count()

    rejected_count = all_bookings.filter(
        status="Rejected"
    ).count()

    cancelled_count = all_bookings.filter(
        status="Cancelled"
    ).count()

    total_count = all_bookings.count()

    selected_status = request.GET.get(
        "status",
        "All"
    )

    valid_statuses = [
        "Pending",
        "Accepted",
        "Completed",
        "Rejected",
        "Cancelled"
    ]

    if selected_status in valid_statuses:

        bookings = all_bookings.filter(
            status=selected_status
        )

    else:

        selected_status = "All"

        bookings = all_bookings

    bookings = bookings.order_by(
        "-created_at"
    )

    for booking in bookings:

        profile, created = CustomerProfile.objects.get_or_create(
            user=booking.customer
        )

        booking.customer_phone = profile.phone

    return render(
        request,
        "provider_dashboard.html",
        {
            "provider": provider,
            "bookings": bookings,
            "pending_count": pending_count,
            "accepted_count": accepted_count,
            "completed_count": completed_count,
            "rejected_count": rejected_count,
            "cancelled_count": cancelled_count,
            "total_count": total_count,
            "selected_status": selected_status,
        }
    )


@login_required
def update_booking_status(
    request,
    booking_id,
    status
):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if booking.provider.user != request.user:
        return redirect("home")

    if booking.status == "Pending":

        if status in [
            "Accepted",
            "Rejected"
        ]:

            booking.status = status
            booking.save()

    elif booking.status == "Accepted":

        if status == "Completed":

            booking.status = status
            booking.save()

    return redirect(
        "provider_dashboard"
    )


@login_required
def cancel_booking(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if request.method == "POST":

        if booking.status == "Pending":

            booking.status = "Cancelled"
            booking.save()

        return redirect(
            "my_bookings"
        )

    return redirect(
        "my_bookings"
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings
        }
    )


@login_required
def add_review(
    request,
    provider_id
):

    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id
    )

    completed_booking = Booking.objects.filter(
        customer=request.user,
        provider=provider,
        status="Completed"
    ).exists()

    if not completed_booking:

        return render(
            request,
            "add_review.html",
            {
                "provider": provider,
                "error": (
                    "You can review this provider only "
                    "after your booking is completed."
                )
            }
        )

    existing_review = Review.objects.filter(
        customer=request.user,
        provider=provider
    ).first()

    if existing_review:

        return redirect(
            "provider_reviews",
            provider_id=provider.id
        )

    if request.method == "POST":

        rating = request.POST.get("rating")
        review_text = request.POST.get("review")

        try:

            rating = int(rating)

        except (
            TypeError,
            ValueError
        ):

            return render(
                request,
                "add_review.html",
                {
                    "provider": provider,
                    "error": (
                        "Please select a valid rating."
                    )
                }
            )

        if rating < 1 or rating > 5:

            return render(
                request,
                "add_review.html",
                {
                    "provider": provider,
                    "error": (
                        "Rating must be between 1 and 5."
                    )
                }
            )

        Review.objects.create(
            customer=request.user,
            provider=provider,
            rating=rating,
            review=review_text
        )

        return redirect(
            "provider_reviews",
            provider_id=provider.id
        )

    return render(
        request,
        "add_review.html",
        {
            "provider": provider
        }
    )


def provider_reviews(
    request,
    provider_id
):

    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id
    )

    reviews = Review.objects.filter(
        provider=provider
    ).order_by(
        "-created_at"
    )

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
        "provider_reviews.html",
        {
            "provider": provider,
            "reviews": reviews,
            "average_rating": average_rating,
            "review_count": reviews.count()
        }
    )


def provider_detail(
    request,
    provider_id
):

    provider = get_object_or_404(
        ServiceProvider,
        id=provider_id
    )

    reviews = Review.objects.filter(
        provider=provider
    ).order_by(
        "-created_at"
    )

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


@login_required
def payment_page(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "customer": request.user,
            "amount": booking.provider.price,
            "payment_status": "Pending"
        }
    )

    if payment.payment_status == "Paid":

        return redirect(
            "payment_success",
            booking_id=booking.id
        )

    error = None

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment_method"
        )

        if not payment_method:

            error = "Please select a payment method."

        else:

            payment.payment_method = payment_method

            payment.payment_status = "Paid"

            payment.transaction_id = (
                "DEMO"
                + str(booking.id)
                + str(
                    int(
                        timezone.now().timestamp()
                    )
                )
            )

            payment.paid_at = timezone.now()

            payment.save()

            return redirect(
                "payment_success",
                booking_id=booking.id
            )

    return render(
        request,
        "payment.html",
        {
            "booking": booking,
            "payment": payment,
            "error": error
        }
    )


@login_required
def payment_success(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    payment = Payment.objects.filter(
        booking=booking
    ).first()

    return render(
        request,
        "payment_success.html",
        {
            "booking": booking,
            "payment": payment
        }
    )