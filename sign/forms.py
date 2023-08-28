import random

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.mail import send_mail

from .models import MyUser, OneTimeCode


class BaseRegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ["username",
                  "full_name",
                  "email",
                  "birhtday",
                  "gender",
                  "mailing",
                  ]


class VerifiedCodeForm(forms.Form):
    verified_fieid = forms.CharField()

