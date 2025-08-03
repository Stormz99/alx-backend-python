from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message

@receiver(post_save, sender=Message)
def notify_receiver_on_message(sender, instance, created, **kwargs):
    if created:
        print(f"Notification: New message for {instance.receiver.username} from {instance.sender.username}")