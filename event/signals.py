from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail

from .models import RSVP


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    groups = ['Admin', 'Organizer', 'Participant']
    for group in groups:
        Group.objects.get_or_create(name=group)

@receiver(post_save, sender=User)
def send_account_activation_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            subject='Account Activated',
            message=(
                f'Hello {instance.username},\n\n'
                f'Your account has been successfully created.\n'
                f'You can now login to your dashboard.'
            ),
            from_email='your_email@gmail.com',
            recipient_list=[instance.email],
            fail_silently=True,
        )
@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='RSVP Confirmation',
            message=(
                f'Hello {instance.user.username},\n\n'
                f'You have successfully RSVP’d for the event:\n'
                f'Event Name: {instance.event.name}\n'
                f'Date: {instance.event.date}\n'
                f'Location: {instance.event.location}\n\n'
                f'Thank you for your participation!'
            ),
            from_email='your_email@gmail.com',
            recipient_list=[instance.user.email],
            fail_silently=True,
        )

