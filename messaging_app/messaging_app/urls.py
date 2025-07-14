#!/usr/bin/env python3
"""
Main URL configuration for messaging_app project.

Includes:
- Admin site
- API routes from chats app under /api/
- DRF authentication under /api-auth/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # ✅ Required: "api/"
    path('api-auth/', include('rest_framework.urls')),  # DRF login view
]
