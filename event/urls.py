# # from django.contrib import admin
# from django.urls import path
# from event import views

# urlpatterns = [

#     # --------------------
#     # Public / Participants
#     # --------------------

#     path('', views.event_list, name='event_list'),
#     path('events/<int:event_id>/', views.event_detail),
#     path('participants/', views.participant_list),

#     # --------------------
#     # Event Management (Organizer + Admin)
#     # --------------------
#     path('events/create/', views.event_create, name='event_create'),
#     path('events/update/<int:event_id>/',
#          views.event_update, name='event_update'),
#     path('events/delete/<int:event_id>/',
#          views.event_delete, name='event_delete'),

#     # --------------------
#     # Category Management (Organizer + Admin)
#     # --------------------
#     path('categories/', views.category_list, name='category_list'),
#     path('categories/create/', views.category_create, name='category_create'),
#     path('categories/update/<int:category_id>/',
#          views.category_update, name='category_update'),
#     path('categories/delete/<int:category_id>/',
#          views.category_delete, name='category_delete'),

#     # --------------------
#     # Admin Dashboard
#     # --------------------
#     path('dashboard/', views.admin_dashboard, name='dashboard'),

#     # --------------------
#     # User & Role Management (Admin only)
#     # --------------------
#     path('admin/users/', views.user_list, name='user_list'),
#     path('admin/users/change-role/<int:user_id>/',
#          views.change_role, name='change_role'),

#     path('admin/groups/', views.group_list, name='group_list'),
#     path('admin/groups/create/', views.group_create, name='group_create'),
#     path('admin/groups/delete/<int:group_id>/',
#          views.group_delete, name='group_delete'),

#     # --------------------
#     # Authentication
#     # --------------------
#     path('signup/', views.signup_view, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]

from django.urls import path
from django.contrib import admin

from event import views

urlpatterns = [
     path('admin/', admin.site.urls),

    # --------------------
    # Public / Participants
    # --------------------
    path('', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('participants/', views.participant_list, name='participant_list'),

    # --------------------
    # Event Management (Organizer + Admin)
    # --------------------
    path('events/create/', views.event_create, name='event_create'),
    path('events/update/<int:event_id>/',
         views.event_update, name='event_update'),
    path('events/delete/<int:event_id>/',
         views.event_delete, name='event_delete'),

    # --------------------
    # Category Management (Organizer + Admin)
    # --------------------
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:category_id>/',
         views.category_update, name='category_update'),
    path('categories/delete/<int:category_id>/',
         views.category_delete, name='category_delete'),

    # --------------------
    # Dashboard (Organizer + Admin)
    # --------------------
    path('dashboard/', views.dashboard, name='dashboard'),

    # --------------------
    # User & Role Management (Admin only)
    # --------------------
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/change-role/<int:user_id>/',
         views.change_role, name='change_role'),
    path('admin/groups/', views.group_list, name='group_list'),
    path('admin/groups/create/', views.group_create, name='group_create'),
    path('admin/groups/delete/<int:group_id>/',
         views.group_delete, name='group_delete'),

    # --------------------
    # Authentication
    # --------------------
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
