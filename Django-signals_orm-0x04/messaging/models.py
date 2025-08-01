from django.db import models
from django.contrib.auth.models import User
import uuid
from .managers import UnreadMessagesManager

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    parent_message = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

def __str__(self):
        return f"{self.sender} ➝ {self.receiver} ({'Reply' if self.parent_message else 'Message'})"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"🔔 Notification for {self.user.username} - Message from {self.message.sender.username}"
