from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings

# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True
    )

    def clean(self):
        super().clean()
        if self.phone_number:
            if not self.phone_number.isdigit():
                raise ValidationError("Phone number must contain only digits.")
            if len(self.phone_number) < 10 or len(self.phone_number) > 15:
                raise ValidationError("Phone number must be 10–15 digits long.")

    def __str__(self):
        return self.username


# -------------------------
# Category Model
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# -------------------------
# Event Model
# -------------------------
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='events'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events'
    )

    rsvps = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='rsvp_events'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
