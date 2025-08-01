import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages sent between date ranges
    sent_at_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_at_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    # Filter by conversation participant username (filter messages where sender is a user)
    sender_email = django_filters.CharFilter(field_name="sender__email", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender_email', 'sent_at_after', 'sent_at_before']
