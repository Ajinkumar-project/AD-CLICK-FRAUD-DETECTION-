from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter_name", "fraud_type", "status", "created_at")
    list_filter = ("fraud_type", "status", "created_at")
    search_fields = ("reporter_name", "reporter_email", "suspected_ip", "click_url")
    readonly_fields = ("created_at", "updated_at")
