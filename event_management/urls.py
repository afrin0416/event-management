"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
