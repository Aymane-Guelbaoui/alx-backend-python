from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . models import Message, Notification
from django.contrib.auth.models import User

@receiver(post_save,sender=Message)
def message_created_handler(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f"✅ New message sent from {instance.sender} to {instance.receiver} at {instance.sent_at}")
        # You can send notifications, emails, or update other models here.
        
@receiver(post_delete,sender=User)
def  user_delete(sender,instance,**kwargs):
    print(f"User {instance.username} deleted. Cleaning up related data.")
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
