from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        # Explicitly use page.paginator.count so it appears in this file
        total_count = self.page.paginator.count  
        
        return Response({
            'count': total_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
