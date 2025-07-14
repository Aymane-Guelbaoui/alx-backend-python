#!/usr/bin/env python3
"""
Models for the chats app in the messaging_app project.

This module defines:
- User: custom user model with UUID primary key and extended fields
- Conversation: conversation between multiple users
- Message: messages sent in conversations
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending AbstractUser with a UUID primary key.

    Fields:
    - user_id: UUID, primary key
    - email: unique email for login
    - password: inherited from AbstractUser
    - first_name: user first name
    - last_name: user last name
    - phone_number: optional phone number
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """
    Represents a conversation involving multiple participants.

    Fields:
    - conversation_id: UUID, primary key
    - participants: many-to-many relationship with User
    - created_at: timestamp when conversation was created
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Represents a message sent by a user in a conversation.

    Fields:
    - message_id: UUID, primary key
    - conversation: foreign key to Conversation
    - sender: foreign key to User
    - message_body: content of the message
    - sent_at: timestamp when message was sent
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
