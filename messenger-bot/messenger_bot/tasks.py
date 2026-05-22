import requests
from django.conf import settings
from .models import Announcement, AnnouncementLog, MessengerGroup
import logging

logger = logging.getLogger(__name__)


def send_scheduled_announcements():
    """
    Check for announcements that need to be sent and send them
    This task runs every minute via Celery Beat
    """
    announcements = Announcement.objects.filter(is_active=True)
    
    for announcement in announcements:
        if announcement.should_send_today():
            send_announcement_to_groups(announcement.id)


def send_announcement_to_groups(announcement_id):
    """
    Send a single announcement to all assigned groups
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        groups = announcement.groups.all()
        
        for group in groups:
            send_to_group(announcement_id, group.id)
            
    except Announcement.DoesNotExist:
        logger.error(f"Announcement {announcement_id} not found")


def send_to_group(announcement_id, group_id):
    """
    Send announcement to a specific group
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        group = MessengerGroup.objects.get(id=group_id)
        
        # Create log entry
        log = AnnouncementLog.objects.create(
            announcement=announcement,
            group=group,
            status='pending'
        )
        
        # Send message via Facebook Messenger API
        success = send_messenger_message(
            recipient_id=group.group_id,
            message=announcement.message
        )
        
        if success:
            log.status = 'success'
            announcement.last_sent = timezone.now()
            announcement.save()
            logger.info(f"Announcement '{announcement.title}' sent to group '{group.group_name}'")
        else:
            log.status = 'failed'
            log.error_message = "Failed to send message via Messenger API"
            logger.error(f"Failed to send announcement '{announcement.title}' to group '{group.group_name}'")
        
        log.save()
        
    except (Announcement.DoesNotExist, MessengerGroup.DoesNotExist) as e:
        logger.error(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in send_to_group: {str(e)}")


def send_messenger_message(recipient_id, message):
    """
    Send message to Messenger using Facebook Graph API
    """
    try:
        # Check if token is configured
        if not settings.FACEBOOK_PAGE_ACCESS_TOKEN or settings.FACEBOOK_PAGE_ACCESS_TOKEN == 'PASTE_YOUR_REAL_TOKEN_HERE':
            logger.error("Facebook page access token not configured. Please set FACEBOOK_PAGE_ACCESS_TOKEN in .env")
            return False

        url = f"https://graph.facebook.com/{settings.FACEBOOK_API_VERSION}/me/messages?access_token={settings.FACEBOOK_PAGE_ACCESS_TOKEN}"
        payload = {
            'recipient': {'id': recipient_id},
            'message': {'text': message}
        }

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Message sent successfully. Recipient: {recipient_id}, Message ID: {data.get('message_id')}")
            return True
        else:
            logger.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while sending message: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in send_messenger_message: {str(e)}")
        return False


def receive_webhook(event_data):
    """
    Handle incoming webhook events from Facebook Messenger
    """
    try:
        # Handle group membership changes, etc.
        logger.info(f"Webhook received: {event_data}")
        # Add your webhook handling logic here
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")


from django.utils import timezone
