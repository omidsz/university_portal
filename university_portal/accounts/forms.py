from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("فقط ایمیل Gmail مجاز است.")
        return email


class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6, label="کد ارسال‌شده به ایمیل")


class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل")

    def clean_email(self):
        email = self.cleaned_data['email']
        print("CLEAN EMAIL CALLED WITH:", email)
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("فقط ایمیل Gmail مجاز است.")
        return email
