from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from .models import Event, Category
from .forms import (
    EventForm,
    CategoryForm,
    CustomUserCreationForm,
    CreateGroupForm
)
from .decorators import group_required, admin_only

# -----------------------
# Participant Views
# -----------------------

def event_list(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.select_related('category')

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if category_id:
        events = events.filter(category_id=category_id)

    if start_date:
        events = events.filter(date__gte=parse_date(start_date))

    if end_date:
        events = events.filter(date__lte=parse_date(end_date))

    categories = Category.objects.all()
    category_selected = request.GET.get('category')

    for cat in categories:
        cat.is_selected = str(cat.id) == category_selected

    return render(request, 'events/eventList.html', {
        'events': events,
        'categories': categories,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/eventDetail.html', {'event': event})



@login_required
@group_required('Participant')
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Prevent duplicate RSVP
    if event.rsvps.filter(id=user.id).exists():
        messages.warning(request, "You have already RSVP’d to this event.")
        return redirect('event_detail', event_id=event.id)

    event.rsvps.add(user)
    messages.success(request, "RSVP successful!")

    # Send confirmation email (console backend)
    send_mail(
        subject=f"RSVP Confirmation for {event.name}",
        message=f"Hi {user.username},\n\nYou have successfully RSVP’d for {event.name} on {event.date} at {event.location}.\n\nThank you!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True
    )

    return redirect('event_detail', event_id=event.id)


@login_required
@group_required('Participant')
def participant_dashboard(request):
    rsvp_events = request.user.rsvp_events.all()
    return render(request, 'events/participant_dashboard.html', {
        'rsvp_events': rsvp_events
    })


# -----------------------
# Event Management (Organizer + Admin)
# -----------------------

@login_required
@group_required('Organizer', 'Admin')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/eventForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/eventForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('event_list')


# -----------------------
# Category Management (Organizer + Admin)
# -----------------------

@login_required
@group_required('Organizer', 'Admin')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/categoryList.html', {'categories': categories})


@login_required
@group_required('Organizer', 'Admin')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/categoryForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/categoryForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('category_list')


# -----------------------
# Dashboard (Organizer + Admin)
# -----------------------

@login_required
@group_required('Organizer', 'Admin')
def dashboard(request):
    total_events = Event.objects.count()
    total_participants = User.objects.filter(
        groups__name='Participant'
    ).count()

    today = timezone.now().date()

    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    })


# -----------------------
# Email Activation
# -----------------------

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate until email activation
            user.save()

            # add to Participant group
            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)

            # send activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                f'/activate/{uid}/{token}/'
            )
            message = render_to_string('events/activation_email.html', {
                'user': user,
                'activation_link': activation_link
            })
            send_mail(
                subject='Activate Your Account',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )

            messages.success(request, "Account created! Check your email to activate your account.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can now login.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('signup')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Your account is not activated. Check your email.")
                return redirect('login')
            login(request, user)
            return redirect('event_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------
# Participant List (Admin only)
# -----------------------

@login_required
@admin_only
def participant_list(request):
    participants = User.objects.filter(groups__name='Participant')
    return render(request, 'events/participantList.html', {
        'participants': participants
    })


@login_required
@admin_only
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'events/group_list.html', {'groups': groups})


@login_required
@admin_only
def group_create(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully.")
            return redirect('group_list')
    else:
        form = CreateGroupForm()
    return render(request, 'events/group_form.html', {'form': form})


@login_required
@admin_only
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully.")
    return redirect('group_list')


@login_required
@admin_only
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})


@login_required
@admin_only
def change_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        group_name = request.POST.get('group')
        user.groups.clear()
        user.groups.add(Group.objects.get(name=group_name))
        messages.success(request, "User role updated successfully.")
        return redirect('user_list')

    return render(request, 'events/change_role.html', {
        'user': user,
        'groups': groups
    })
