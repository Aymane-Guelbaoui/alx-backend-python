from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        # fields = ['__all__']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info
    message_body = serializers.CharField()  # explicit CharField for message body
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True,
        help_text="List of user UUIDs to be participants"
    )
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'message_count', 'participant_ids']

    def get_message_count(self, obj):
        return obj.messages.count()

    def validate(self, data):
        print("VALIDATION DEBUG:", data)
        participant_ids = data.get('participant_ids', [])
        if not participant_ids:
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return data


    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        return conversation
