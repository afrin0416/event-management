from django.contrib import admin
from django.urls import path
from event import views
from django.conf import settings
from django.conf.urls.static import static
from event.views import EventCreateView,EventUpdateView, EventDeleteView
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),

    # --------------------
    #  Participants
    # --------------------
    
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:event_id>/',views.EventDetailView.as_view(), name='event_detail'),
  
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),  
    path('participant/dashboard/', views.participant_dashboard, name='participant_dashboard'),  
    path('participants/', views.participant_list, name='participant_list'), 
    # --------------------
    # Event Management (Organizer + Admin)
    # --------------------
    path('create/', EventCreateView.as_view(), name='event_create'),

    path('events/update/<int:event_id>/', EventUpdateView.as_view(), name='event_update'),

    path('events/delete/<int:event_id>/', EventDeleteView.as_view(), name='event_delete'),

    # --------------------
    # Category Management (Organizer + Admin)
    # --------------------
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:category_id>/', views.category_update, name='category_update'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='category_delete'),

    # --------------------
    # Dashboard (Organizer + Admin)
    # --------------------
    path('dashboard/', views.dashboard, name='dashboard'),

    # --------------------
    # User & Role Management (Admin only)
    # --------------------
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/change-role/<int:user_id>/', views.change_role, name='change_role'),
    path('admin/groups/', views.group_list, name='group_list'),
    path('admin/groups/create/', views.group_create, name='group_create'),
    path('admin/groups/delete/<int:group_id>/', views.group_delete, name='group_delete'),

    # --------------------
    # Authentication
    # --------------------
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --------------------
    # Email Activation
    # --------------------
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('', RedirectView.as_view(pattern_name='event_list', permanent=False)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)