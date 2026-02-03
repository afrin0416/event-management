from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Event

# Custom User
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'profile_pic')}),
    )

# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

# Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'start_time', 'end_time', 'created_by')
    list_filter = ('category', 'date')
    search_fields = ('name', 'location', 'description')
