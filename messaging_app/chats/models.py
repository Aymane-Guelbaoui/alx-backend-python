#!/usr/bin/env python3
"""Models for chats app."""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Extend with additional fields if needed.
    """
    pass


class Conversation(models.Model):
    """
    Model representing a conversation between multiple users.
    """
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with users {[user.username for user in self.users.all()]}"


class Message(models.Model):
    """
    Model representing a message sent by a user in a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} at {self.timestamp}"
