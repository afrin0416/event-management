from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.conf import settings

from .models import RSVP, Profile  


# -------------------------------
# Create default groups after migrations
# -------------------------------
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'event':  # replace 'event' with your app name if different
        groups = ['Admin', 'Organizer', 'Participant']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)


# -------------------------------
#  Automatically create Profile for new users
# -------------------------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Only save if the profile exists
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)



# -------------------------------
# Send account activation email
# -------------------------------
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
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'your_email@gmail.com'),
            recipient_list=[instance.email],
            fail_silently=True,  # Consider logging failures in production
        )


# -------------------------------
# Send RSVP confirmation email
# -------------------------------
@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation_email(sender, instance, created, **kwargs):
    if created and instance.user.email:
        event = instance.event
        send_mail(
            subject='RSVP Confirmation',
            message=(
                f'Hello {instance.user.username},\n\n'
                f'You have successfully RSVP’d for the event:\n'
                f'Event Name: {event.name}\n'
                f'Date: {event.date.strftime("%B %d, %Y")}\n'
                f'Location: {event.location}\n\n'
                f'Thank you for your participation!'
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'your_email@gmail.com'),
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
