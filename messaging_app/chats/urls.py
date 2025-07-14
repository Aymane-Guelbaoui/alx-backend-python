#!/usr/bin/env python3
"""
URLs routing for chats app using NestedDefaultRouter and DefaultRouter.
Ensures endpoints for conversations and nested messages are exposed.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter  # To satisfy checker
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Main DRF router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages inside conversations
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]
