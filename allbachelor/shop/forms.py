from django import forms
from django.forms import ModelForm, Textarea
from .models import Review
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from bootstrap_datepicker_plus import DatePickerInput
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField
from markdownx.fields import MarkdownxFormField
from django import forms

from django.core.validators import MinLengthValidator
from PIL import Image


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 20, 'rows': 5}),
        }


