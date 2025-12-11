from django.contrib import admin
from django.urls import path
from event import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('dashboard/', views.organizer_dashboard, name='dashboard'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:category_id>/',
         views.category_update, name='category_update'),
    path('categories/delete/<int:category_id>/',
         views.category_delete, name='category_delete'),

    path('participants/', views.participant_list, name='participant_list'),
    path('participants/create/', views.participant_create,
         name='participant_create'),
    path('participants/update/<int:participant_id>/',
         views.participant_update, name='participant_update'),
    path('participants/delete/<int:participant_id>/',
         views.participant_delete, name='participant_delete'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Admin role URLs
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/delete/<int:group_id>/',
         views.group_delete, name='group_delete'),

    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('users/change_role/<int:user_id>/',
         views.change_role, name='change_role'),


]
