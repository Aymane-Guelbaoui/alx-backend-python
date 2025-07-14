#!/usr/bin/env python3
"""
Views for chats app using Django REST Framework viewsets.

Includes:
- ConversationViewSet: list, create conversations
- MessageViewSet: list, create messages within a conversation
"""

from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of user IDs in 'participants'.
        """
        participants = request.data.get('participants', [])
        if not participants or not isinstance(participants, list):
            return Response(
                {'error': 'Participants field must be a non-empty list of user IDs.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages in conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['sent_at']

    def create(self, request, *args, **kwargs):
        """
        Create a message linked to a conversation.
        Expects 'conversation' and 'sender' user IDs, and 'message_body'.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
