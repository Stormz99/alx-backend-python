from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
        
@receiver(post_save, sender=Message)
def log_message_edit(sender, instance, created, **kwargs):
    if not created:
        print(f"Message edited: {instance.id} by {instance.sender.username}")