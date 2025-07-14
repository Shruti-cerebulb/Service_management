from django.contrib import admin
from .models import PushSubscription, Notification

@admin.register(PushSubscription)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'created_at')
    search_fields = ('user__username', 'endpoint')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
