#!/usr/bin/env python3
"""
Serializers for the chats app models.

Includes:
- UserSerializer
- MessageSerializer
- ConversationSerializer with nested messages
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number')


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""

    message_body = serializers.CharField()
    sent_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('message_id', 'message_body', 'sent_at', 'sender')

    def get_sent_at(self, obj):
        """Return ISO format datetime for sent_at."""
        return obj.sent_at.isoformat()


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages."""

    conversation_id = serializers.CharField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    recent_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'messages', 'recent_message')

    def get_recent_message(self, obj):
        """Return the last message body or raise ValidationError if none."""
        last_message = obj.messages.order_by('-sent_at').first()
        if not last_message:
            raise serializers.ValidationError("No messages found in this conversation.")
        return last_message.message_body
