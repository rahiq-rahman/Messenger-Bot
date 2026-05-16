from django.contrib import admin
from .models import Announcement, MessengerGroup, AnnouncementLog


@admin.register(MessengerGroup)
class MessengerGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_id', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['group_name', 'group_id', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('group_id', 'group_name', 'owner')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set owner on creation
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'frequency', 'owner', 'is_active', 'last_sent', 'created_at']
    list_filter = ['frequency', 'is_active', 'created_at', 'frequency']
    search_fields = ['title', 'message', 'owner__username']
    readonly_fields = ['created_at', 'updated_at', 'last_sent']
    filter_horizontal = ['groups']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'message', 'owner')
        }),
        ('Schedule Settings', {
            'fields': ('frequency', 'scheduled_date', 'scheduled_time', 
                      'days_of_week', 'day_of_month'),
            'description': 'Configure when this announcement should be sent'
        }),
        ('Groups', {
            'fields': ('groups',),
            'description': 'Select which groups should receive this announcement'
        }),
        ('Status', {
            'fields': ('is_active', 'last_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set owner on creation
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs


@admin.register(AnnouncementLog)
class AnnouncementLogAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'group', 'sent_at', 'status', 'get_error_preview']
    list_filter = ['status', 'sent_at', 'announcement__frequency']
    search_fields = ['announcement__title', 'group__group_name', 'error_message']
    readonly_fields = ['announcement', 'group', 'sent_at', 'status', 'error_message', 'messenger_timestamp']
    
    fieldsets = (
        ('Announcement Details', {
            'fields': ('announcement', 'group', 'sent_at')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Messenger Info', {
            'fields': ('messenger_timestamp',),
            'classes': ('collapse',)
        }),
    )

    def get_error_preview(self, obj):
        if obj.error_message:
            return obj.error_message[:50] + '...' if len(obj.error_message) > 50 else obj.error_message
        return '—'
    get_error_preview.short_description = 'Error'

    def has_add_permission(self, request):
        return False  # Logs are created automatically

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(announcement__owner=request.user)
        return qs
