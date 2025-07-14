#!/usr/bin/env python3
"""
Models for the chats app of messaging_app project.

Defines:
- User: Custom user model extending Django's AbstractUser with extra fields.
- Conversation: Tracks users involved in a conversation.
- Message: Contains sender, conversation, content, and timestamp.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Added 'display_name' field for enhanced user representation.
    """
    display_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional display name for the user."
    )

    def __str__(self):
        return self.display_name or self.username


class Conversation(models.Model):
    """
    Model representing a conversation involving multiple users.
    """
    users = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the conversation was created."
    )

    def __str__(self):
        usernames = ', '.join(user.username for user in self.users.all())
        return f"Conversation ({self.id}) between: {usernames}"


class Message(models.Model):
    """
    Model representing a message sent by a user in a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Conversation this message belongs to."
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent the message."
    )
    content = models.TextField(
        help_text="Content of the message."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was sent."
    )

    def __str__(self):
        return f"Message ({self.id}) from {self.sender} at {self.timestamp}"
