#!/usr/bin/env python3
"""Views for chats app."""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override create to accept list of user IDs to start a conversation.
        """
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response({"detail": "user_ids list is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(id__in=user_ids)
        if users.count() != len(user_ids):
            return Response({"detail": "Some users not found."},
                            status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.users.set(users)
        conversation.users.add(request.user)  # Add current user
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages within a conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        content = request.data.get('content')
        if not conversation_id or not content:
            return Response({"detail": "conversation and content are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.users.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Optionally filter messages by conversation ID via query param.
        """
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return self.queryset.filter(conversation_id=conversation_id)
        return self.queryset.none()  # no messages if no conversation specified
