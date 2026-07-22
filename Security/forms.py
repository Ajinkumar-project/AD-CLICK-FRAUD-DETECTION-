from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Complaint


class ComplaintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = "form-select" if name == "fraud_type" else "form-control"
            field.widget.attrs["class"] = css_class

    class Meta:
        model = Complaint
        fields = [
            "reporter_name",
            "reporter_email",
            "reporter_phone",
            "click_url",
            "suspected_ip",
            "fraud_type",
            "description",
            "evidence_link",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Enter username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Enter password"}
        )


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Choose username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Create password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Confirm password"}
        )
