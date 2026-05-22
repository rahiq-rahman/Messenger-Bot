from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messenger_bot import views

# REST API Router
router = DefaultRouter()
router.register(r'announcements', views.AnnouncementViewSet, basename='announcement')
router.register(r'groups', views.MessengerGroupViewSet, basename='group')
router.register(r'logs', views.AnnouncementLogViewSet, basename='log')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Announcements URLs
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),

    # Groups URLs
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),

    # Logs URLs
    path('logs/', views.logs_view, name='logs'),

    # Messenger Webhook
    path('webhook/', views.messenger_webhook, name='messenger_webhook'),
    
    # Cron Trigger
    path('cron/trigger-announcements/<str:secret_key>/', views.trigger_announcements, name='trigger_announcements'),

    # API URLs
    path('api/', include(router.urls)),
]

# Admin site customization
admin.site.site_header = "Messenger Bot Admin"
admin.site.site_title = "Messenger Bot"
admin.site.index_title = "Welcome to Messenger Bot Admin"
