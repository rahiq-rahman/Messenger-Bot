from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import logging
import hmac
import hashlib
import os

from .models import Announcement, MessengerGroup, AnnouncementLog
from .serializers import AnnouncementSerializer, MessengerGroupSerializer, AnnouncementLogSerializer
from .forms import AnnouncementForm, MessengerGroupForm
from django.conf import settings

logger = logging.getLogger(__name__)


# Authentication Views
def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


# Dashboard Views
@login_required(login_url='login')
def dashboard(request):
    """Main dashboard showing announcements and groups"""
    announcements = Announcement.objects.filter(owner=request.user)
    groups = MessengerGroup.objects.filter(owner=request.user)
    logs = AnnouncementLog.objects.filter(announcement__owner=request.user).order_by('-sent_at')[:10]

    context = {
        'announcements': announcements,
        'groups': groups,
        'logs': logs,
        'total_announcements': announcements.count(),
        'total_groups': groups.count(),
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def announcements_list(request):
    """List all announcements"""
    announcements = Announcement.objects.filter(owner=request.user).prefetch_related('groups')
    context = {'announcements': announcements}
    return render(request, 'announcements/list.html', context)


@login_required(login_url='login')
def announcement_create(request):
    """Create new announcement"""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, user=request.user)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.owner = request.user
            announcement.save()
            form.save_m2m()
            messages.success(request, 'Announcement created successfully!')
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(user=request.user)

    context = {'form': form}
    return render(request, 'announcements/form.html', context)


@login_required(login_url='login')
def announcement_edit(request, pk):
    """Edit existing announcement"""
    announcement = get_object_or_404(Announcement, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully!')
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(instance=announcement, user=request.user)

    context = {'form': form, 'announcement': announcement}
    return render(request, 'announcements/form.html', context)


@login_required(login_url='login')
def announcement_delete(request, pk):
    """Delete announcement"""
    announcement = get_object_or_404(Announcement, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully!')
        return redirect('announcements_list')

    context = {'announcement': announcement}
    return render(request, 'announcements/confirm_delete.html', context)


@login_required(login_url='login')
def groups_list(request):
    """List all messenger groups"""
    groups = MessengerGroup.objects.filter(owner=request.user)
    context = {'groups': groups}
    return render(request, 'groups/list.html', context)


@login_required(login_url='login')
def group_create(request):
    """Create new messenger group"""
    if request.method == 'POST':
        form = MessengerGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            messages.success(request, 'Group created successfully!')
            return redirect('groups_list')
    else:
        form = MessengerGroupForm()

    context = {'form': form}
    return render(request, 'groups/form.html', context)


@login_required(login_url='login')
def group_edit(request, pk):
    """Edit messenger group"""
    group = get_object_or_404(MessengerGroup, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = MessengerGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated successfully!')
            return redirect('groups_list')
    else:
        form = MessengerGroupForm(instance=group)

    context = {'form': form, 'group': group}
    return render(request, 'groups/form.html', context)


@login_required(login_url='login')
def group_delete(request, pk):
    """Delete messenger group"""
    group = get_object_or_404(MessengerGroup, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully!')
        return redirect('groups_list')

    context = {'group': group}
    return render(request, 'groups/confirm_delete.html', context)


@login_required(login_url='login')
def logs_view(request):
    """View announcement sending logs"""
    logs = AnnouncementLog.objects.filter(
        announcement__owner=request.user
    ).select_related('announcement', 'group').order_by('-sent_at')
    
    context = {'logs': logs}
    return render(request, 'logs.html', context)


# Messenger Webhook Handling
@csrf_exempt
@require_http_methods(["GET", "POST"])
def messenger_webhook(request):
    """
    Handle webhook from Facebook Messenger
    GET: Verify token
    POST: Process incoming messages and events
    """
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if verify_token == settings.FACEBOOK_VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('Invalid verification token', status=403)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Verify webhook signature
            x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE', '')
            if not verify_webhook_signature(request.body, x_hub_signature):
                logger.warning("Invalid webhook signature")
                return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=403)

            # Process webhook events
            if data.get('object') == 'page':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        # Handle different types of events
                        if messaging_event.get('message'):
                            handle_message(messaging_event)
                        elif messaging_event.get('postback'):
                            handle_postback(messaging_event)

            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def verify_webhook_signature(payload, x_hub_signature):
    """Verify Facebook webhook signature"""
    try:
        hash_algorithm, signature = x_hub_signature.split('=')
        expected_signature = hmac.new(
            settings.FACEBOOK_PAGE_ACCESS_TOKEN.encode(),
            payload,
            hashlib.sha1
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except:
        return False


def handle_message(event):
    """Handle incoming messages"""
    sender_id = event.get('sender', {}).get('id')
    message_text = event.get('message', {}).get('text', '')
    
    logger.info(f"Received message from {sender_id}: {message_text}")
    # Add your message handling logic here


def handle_postback(event):
    """Handle postback events"""
    sender_id = event.get('sender', {}).get('id')
    postback_payload = event.get('postback', {}).get('payload', '')
    
    logger.info(f"Received postback from {sender_id}: {postback_payload}")
    # Add your postback handling logic here


# REST API ViewSets
class AnnouncementViewSet(viewsets.ModelViewSet):
    """API endpoints for announcements"""
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        announcement = self.get_object()
        announcement.is_active = not announcement.is_active
        announcement.save()
        return Response({'is_active': announcement.is_active})

    @action(detail=False)
    def active(self, request):
        active_announcements = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_announcements, many=True)
        return Response(serializer.data)


class MessengerGroupViewSet(viewsets.ModelViewSet):
    """API endpoints for messenger groups"""
    serializer_class = MessengerGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MessengerGroup.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnnouncementLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for announcement logs"""
    serializer_class = AnnouncementLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnnouncementLog.objects.filter(
            announcement__owner=self.request.user
        ).order_by('-sent_at')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def trigger_announcements(request, secret_key):
    """
    Endpoint for external cron services to trigger announcements.
    """
    expected_key = os.environ.get('CRON_SECRET_KEY')
    if not expected_key or secret_key != expected_key:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
    from .tasks import send_scheduled_announcements
    send_scheduled_announcements()
    
    return JsonResponse({'status': 'success', 'message': 'Announcements processed'})
