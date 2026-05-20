from django import forms
from .models import Announcement, MessengerGroup


class MessengerGroupForm(forms.ModelForm):
    """Form for creating and editing Messenger groups"""
    
    class Meta:
        model = MessengerGroup
        fields = ['group_id', 'group_name', 'is_active']
        widgets = {
            'group_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Facebook Group/Chat ID',
                'help_text': 'You can find this in the URL when viewing the group'
            }),
            'group_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter group name'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_id'].label = 'Group ID (Facebook Group/Chat ID)'
        self.fields['group_name'].label = 'Group Name'


class AnnouncementForm(forms.ModelForm):
    """Form for creating and editing announcements"""
    
    class Meta:
        model = Announcement
        fields = [
            'title',
            'message',
            'frequency',
            'scheduled_date',
            'scheduled_time',
            'days_of_week',
            'day_of_month',
            'groups',
            'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter announcement title',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter your announcement message here',
                'required': True
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control',
                'id': 'frequency-select',
                'required': True
            }),
            'scheduled_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'scheduled_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'value': '09:00',
            }),
            'days_of_week': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mon,Wed,Fri (for weekly announcements)',
            }),
            'day_of_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1-31 (for monthly announcements)',
                'min': '1',
                'max': '31',
            }),
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter groups to show only user's groups
        if user:
            self.fields['groups'].queryset = MessengerGroup.objects.filter(owner=user)
        
        # Add help texts
        self.fields['scheduled_time'].help_text = 'Time in HH:MM format (24-hour)'
        self.fields['days_of_week'].help_text = 'For weekly: Mon,Tue,Wed,Thu,Fri,Sat,Sun'
        self.fields['day_of_month'].help_text = 'For monthly: Day number (1-31)'

    def clean(self):
        """Custom validation"""
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')
        scheduled_date = cleaned_data.get('scheduled_date')
        days_of_week = cleaned_data.get('days_of_week')
        day_of_month = cleaned_data.get('day_of_month')

        # Validate based on frequency
        if frequency == 'once' and not scheduled_date:
            raise forms.ValidationError('Please select a date for one-time announcements.')
        
        if frequency == 'weekly' and not days_of_week:
            raise forms.ValidationError('Please specify days of week (Mon,Tue,Wed,Thu,Fri,Sat,Sun).')
        
        if frequency == 'monthly' and not day_of_month:
            raise forms.ValidationError('Please specify day of month (1-31).')

        # Validate days_of_week format
        if days_of_week:
            valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            provided_days = [d.strip().lower() for d in days_of_week.split(',')]
            if not all(day in valid_days for day in provided_days):
                raise forms.ValidationError('Invalid day format. Use: Mon,Tue,Wed,Thu,Fri,Sat,Sun')

        # Validate day_of_month
        if day_of_month and (day_of_month < 1 or day_of_month > 31):
            raise forms.ValidationError('Day of month must be between 1 and 31.')

        return cleaned_data
