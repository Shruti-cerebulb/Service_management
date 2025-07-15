from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Notification
from service_category.models import Booking
from .utils import send_push_notification

@receiver(post_save, sender=Booking)
def booking_created_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        service = instance.service
        employee = instance.employee 
        scheduled_datetime = instance.scheduled_date.strftime("%d %B %Y at %I:%M %p")

        user_title = "Booking Confirmed ✅"
        user_message = (
            f"Hi {user.username}, your booking for {service.name} is confirmed "
            f"on {scheduled_datetime}."
        )

        Notification.objects.create(
            user=user,
            title=user_title,
            message=user_message,
            trigger_event="booking_created"
        )
        send_push_notification(
            user=user,
            title=user_title,
            message=user_message,
            url="/bookings/"
        )
        # To Notify employee
        if employee:
            emp_title = "New Booking Assigned 📅"
            emp_message = (
                f"You have a new booking from {user.username} for {service.name} "
                f"on {scheduled_datetime}."
            )

            Notification.objects.create(
                user=employee.user, 
                title=emp_title,
                message=emp_message,
                trigger_event="booking_assigned"
            )
            send_push_notification(
                user=employee.user,
                title=emp_title,
                message=emp_message,
                url="/employee/bookings/"
            )