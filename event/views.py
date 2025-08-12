from django.shortcuts import render, redirect
from .models import Event, Participant, Category
from django.db.models import Q, Count
from django.utils.dateparse import parse_date
from django.utils import timezone
from .forms import EventForm, ParticipantForm, CategoryForm

# Event Views


def index(request):
    return render(request, 'base.html')


def event_list(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.select_related(
        'category').prefetch_related('participants')

    # Search by name or location
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # Filter by category
    if category_id:
        events = events.filter(category_id=category_id)

    # Date range
    if start_date:
        events = events.filter(date__gte=parse_date(start_date))
    if end_date:
        events = events.filter(date__lte=parse_date(end_date))

    
    total_participants = Participant.objects.count()

    # Get all categories for the dropdown
    categories = Category.objects.all()

    context = {
        'events': events,
        'total_participants': total_participants,
        'categories': categories,
    }

    return render(request, 'events/eventList.html', context)


def event_detail(request, event_id):
    event = event.objects.get(id=event_id)
    return render(request, 'events/eventDetail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/eventForm.html', {'form': form})


def event_update(request, event_id):
    event = event.objects.get(id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/eventForm.html', {'form': form})


def event_delete(request, event_id):
    event = event.objects.get(id=event_id)
    event.delete()
    return redirect('event_list')


# Participant Views


def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'events/participantList.html', {'participants': participants})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participantList')
    else:
        form = ParticipantForm()
    return render(request, 'events/participantForm.html', {'form': form})


def participant_update(request, participant_id):
    participant = Participant.objects.get(id=participant_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participantList')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participantForm.html', {'form': form})


def participant_delete(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    participant.delete()
    return redirect('participant_list')


# Category Views


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/categoryList.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/categoryForm.html', {'form': form})


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


def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')


# Dashboard View


def organizer_dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    now = timezone.now().date()

    upcoming_events = Event.objects.filter(date__gt=now).count()
    past_events = Event.objects.filter(date__lt=now).count()
    today_events = Event.objects.filter(date=now)

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': today_events,
    }
    return render(request, 'events/dashboard.html', context)
