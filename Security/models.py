from django.db import models


class Complaint(models.Model):
    FRAUD_TYPE_CHOICES = [
        ("click_fraud", "Click Fraud"),
        ("bot_traffic", "Bot Traffic"),
        ("fake_lead", "Fake Lead"),
        ("payment_fraud", "Payment Fraud"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("under_review", "Under Review"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    ]

    reporter_name = models.CharField(max_length=120)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=20, blank=True)
    click_url = models.URLField(blank=True)
    suspected_ip = models.GenericIPAddressField(blank=True, null=True)
    fraud_type = models.CharField(max_length=20, choices=FRAUD_TYPE_CHOICES, default="click_fraud")
    description = models.TextField()
    evidence_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Complaint #{self.pk} - {self.get_fraud_type_display()}"
