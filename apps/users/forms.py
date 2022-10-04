from captcha.fields import ReCaptchaField
from content.utils import ProfanityFilter
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Support, User


class LoginForm(AuthenticationForm):

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both " "fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    username = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Email",
                "class": "form-control mb-3",
            }
        ),
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
                "class": "form-control mb-3",
            }
        ),
    )
    captcha = ReCaptchaField(label="")

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Email",
                "class": "form-control mb-3",
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "class": "form-control mb-3",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password confirmation",
                "class": "form-control mb-3",
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    captcha = ReCaptchaField(label="")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        data = self.cleaned_data["email"]
        email = User.objects.filter(email__iexact=data)
        if email.exists():
            raise ValidationError("Email address is already associated with an existing account.")
        return data


class UserAccountForm(forms.Form):
    username = forms.CharField(
        max_length=75,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    captcha = ReCaptchaField(label="")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")
        if password != password1:
            raise ValidationError({"password": "Passwords do not match. Please double check and try again."})
        return cleaned_data


class SupportForm(ProfanityFilter, forms.ModelForm):
    contact = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Contact"}),
    )
    subject = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Subject"}),
        required=False,
    )
    body = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 5, "cols": 20, "placeholder": "Body"}),
    )
    captcha = ReCaptchaField(label="")

    class Meta:
        model = Support
        fields = "__all__"

    user_text_fields = ["contact", "subject", "body"]
    field_order = ["contact", "subject", "body", "captcha"]
