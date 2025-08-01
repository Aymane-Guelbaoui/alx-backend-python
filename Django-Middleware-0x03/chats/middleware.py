import logging
from datetime import datetime, time,timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse 
from collections import defaultdict
import threading

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)  # You can configure this logger in settings.py

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response        

    def __call__(self, request):
        # Get the current time
        now = datetime.now().time()
         # Define restricted hours: before 6 PM or after 9 PM
        if now < time(18, 0) or now > time(21, 0):
            return HttpResponseForbidden("❌ Access denied: outside allowed hours (6PM - 9PM).")

        # Continue processing
        response = self.get_response(request)
        return response       

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = defaultdict(list)  # Stores timestamps for each IP
        self.lock = threading.Lock()  # Ensures thread safety

    def __call__(self, request):
        # Only apply the rule to POST requests (e.g., sending a chat message)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()

            with self.lock:
                # Clean up old timestamps
                self.requests_log[ip] = [
                    t for t in self.requests_log[ip] if now - t < timedelta(minutes=1)
                ]

                if len(self.requests_log[ip]) >= 5:
                    return JsonResponse(
                        {"error": "❌ Rate limit exceeded. Max 5 messages per minute."},
                        status=429
                    )

                # Log current request time
                self.requests_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        if not user or not user.is_authenticated:
            return JsonResponse({"error": "❌ Unauthorized. Login required."}, status=403)

        # Check user role: assuming roles are managed via user.is_staff or user.groups
        if not (user.is_superuser or user.is_staff):
            return JsonResponse({"error": "❌ Unauthorized. Admin or Moderator only."}, status=403)

        return self.get_response(request)
