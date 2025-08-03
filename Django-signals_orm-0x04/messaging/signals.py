from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from messaging.models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True
        instance.edited_at = timezone.now()

@reciever(post_delete, sender=User)
def cleanup_user_related_user(sender, instance, **kwargs):
    # Deletw sent and recieved messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()
    Notification.objects.filter(message_sender=instance).delete()
    Notification.objects.filter(message_receiver=instance).delete()
    
    #Delete message histories related to the user message
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()