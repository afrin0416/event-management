from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm, CustomUserCreationForm, CreateGroupForm
from .decorators import group_required, admin_only
from .decorators import organizer_only


# -----------------------
# Event Views
# -----------------------

def index(request):
    return render(request, 'base.html')


def event_list(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.select_related('category')

    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    if category_id:
        events = events.filter(category_id=category_id)
    if start_date:
        events = events.filter(date__gte=parse_date(start_date))
    if end_date:
        events = events.filter(date__lte=parse_date(end_date))

    total_participants = Participant.objects.count()
    categories = Category.objects.all()

    return render(request, 'events/eventList.html', {
        'events': events,
        'total_participants': total_participants,
        'categories': categories,
    })


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/eventDetail.html', {'event': event})


@login_required
@group_required('Organizer', 'Admin')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/eventForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/eventForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('event_list')


# -----------------------
# Participant Views
# -----------------------

def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'events/participantList.html', {'participants': participants})


@login_required
@group_required('Organizer', 'Admin')
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participantForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def participant_update(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participantForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def participant_delete(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    participant.delete()
    return redirect('participant_list')


# -----------------------
# Category Views
# -----------------------

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
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/categoryForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def category_update(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/categoryForm.html', {'form': form})


@login_required
@group_required('Organizer', 'Admin')
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')


# -----------------------
# Dashboard
# -----------------------

@login_required
@group_required('Organizer', 'Admin')
def organizer_dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    now = timezone.now().date()

    upcoming_events = Event.objects.filter(date__gt=now).count()
    past_events = Event.objects.filter(date__lt=now).count()
    today_events = Event.objects.filter(date=now)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': today_events,
    })


# -----------------------
# Authentication Views
# -----------------------

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------
# Group & Role Management (Admin only)
# -----------------------

@login_required
@admin_only
def group_create(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully!")
            return redirect('group_list')
    else:
        form = CreateGroupForm()
    return render(request, 'events/group_form.html', {'form': form})


@login_required
@admin_only
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'events/group_list.html', {'groups': groups})


@login_required
@admin_only
def group_delete(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, "Group deleted.")
    return redirect('group_list')


@login_required
@admin_only
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User deleted.")
    return redirect('participant_list')


@login_required
@admin_only
def change_role(request, user_id):
    user = User.objects.get(id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        selected_group = request.POST.get('group')
        user.groups.clear()
        user.groups.add(Group.objects.get(name=selected_group))
        messages.success(request, "User role updated.")
        return redirect('participant_list')

    return render(request, 'events/change_role.html', {'user': user, 'groups': groups})


@login_required
@admin_only
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    role = request.POST.get('role')  # Admin / Organizer / Participant

    group = Group.objects.get(name=role)
    user.groups.clear()
    user.groups.add(group)

    return redirect('user_list')


@login_required
@admin_only
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})



@login_required
@organizer_only
def create_event(request):
    event_list = Event.objects.all()
    return render(request, 'events/create_event.html', {'events': event_list})
    
@login_required
@organizer_only
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, "Event deleted.")
    return redirect('eventList')
@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/eventList.html', {'events': events})
