# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        if not request.user or not request.user.is_authenticated:
            return False
        
         # Allow GET, POST, PUT, PATCH, DELETE only for participants
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()

        return False


class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only if the user is part of the conversation that owns the message.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        if not request.user or not request.user.is_authenticated:
            return False
        
         # Allow GET, POST, PUT, PATCH, DELETE only for participants
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        return False
