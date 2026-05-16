from rest_framework import serializers
from .models import Announcement, MessengerGroup, AnnouncementLog


class MessengerGroupSerializer(serializers.ModelSerializer):
    """Serializer for Messenger Groups"""
    
    class Meta:
        model = MessengerGroup
        fields = [
            'id',
            'group_id',
            'group_name',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for Announcements"""
    
    groups = MessengerGroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=MessengerGroup.objects.all(),
        source='groups'
    )
    last_sent_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'message',
            'frequency',
            'scheduled_date',
            'scheduled_time',
            'days_of_week',
            'day_of_month',
            'groups',
            'group_ids',
            'is_active',
            'last_sent',
            'last_sent_display',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_sent']

    def get_last_sent_display(self, obj):
        """Format last_sent datetime"""
        if obj.last_sent:
            return obj.last_sent.strftime('%Y-%m-%d %H:%M:%S')
        return None

    def validate(self, data):
        """Validate announcement data"""
        frequency = data.get('frequency')
        scheduled_date = data.get('scheduled_date')
        days_of_week = data.get('days_of_week')
        day_of_month = data.get('day_of_month')

        if frequency == 'once' and not scheduled_date:
            raise serializers.ValidationError(
                'scheduled_date is required for one-time announcements'
            )
        
        if frequency == 'weekly' and not days_of_week:
            raise serializers.ValidationError(
                'days_of_week is required for weekly announcements'
            )
        
        if frequency == 'monthly' and not day_of_month:
            raise serializers.ValidationError(
                'day_of_month is required for monthly announcements'
            )

        return data


class AnnouncementLogSerializer(serializers.ModelSerializer):
    """Serializer for Announcement Logs"""
    
    announcement_title = serializers.CharField(
        source='announcement.title',
        read_only=True
    )
    group_name = serializers.CharField(
        source='group.group_name',
        read_only=True
    )
    sent_at_display = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnouncementLog
        fields = [
            'id',
            'announcement',
            'announcement_title',
            'group',
            'group_name',
            'sent_at',
            'sent_at_display',
            'status',
            'error_message',
            'messenger_timestamp'
        ]
        read_only_fields = [
            'sent_at',
            'status',
            'error_message',
            'messenger_timestamp'
        ]

    def get_sent_at_display(self, obj):
        """Format sent_at datetime"""
        return obj.sent_at.strftime('%Y-%m-%d %H:%M:%S')
