from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Complaint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reporter_name", models.CharField(max_length=120)),
                ("reporter_email", models.EmailField(max_length=254)),
                ("reporter_phone", models.CharField(blank=True, max_length=20)),
                ("click_url", models.URLField(blank=True)),
                ("suspected_ip", models.GenericIPAddressField(blank=True, null=True)),
                (
                    "fraud_type",
                    models.CharField(
                        choices=[
                            ("click_fraud", "Click Fraud"),
                            ("bot_traffic", "Bot Traffic"),
                            ("fake_lead", "Fake Lead"),
                            ("payment_fraud", "Payment Fraud"),
                            ("other", "Other"),
                        ],
                        default="click_fraud",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                ("evidence_link", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("under_review", "Under Review"),
                            ("resolved", "Resolved"),
                            ("rejected", "Rejected"),
                        ],
                        default="new",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
