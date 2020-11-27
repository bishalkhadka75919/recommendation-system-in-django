from django import forms
from django.forms import ModelForm, Textarea

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from bootstrap_datepicker_plus import DatePickerInput
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField
from markdownx.fields import MarkdownxFormField
from django import forms
from .models import Profile
from django.core.validators import MinLengthValidator
from PIL import Image



class ProfileForm(forms.ModelForm):
    """Profile Form + Fields for Photo Processing"""
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    bio = MarkdownxFormField(validators=[MinLengthValidator(10)])

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'email_verify',
            'date_of_birth',
            'bio',
            'city',
            'district',
            'country_of_residence',
            'hobby',
            'avatar',
            'x',
            'y',
            'width',
            'height',
        ]
        widgets = {
            # default date-format %m/%d/%Y will be used
            'date_of_birth': DatePickerInput(),
        }

    def clean(self):
        """Clean the whole form"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('email_verify')

        if email != verify:
            raise forms.ValidationError('Emails do not match')

    def save(self):
        """Override the Save method for saving the crop photo"""
        photo = super().save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if x is not None:
            image = Image.open(photo.avatar)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.avatar.path)
        return photo


class CustomChangePasswordForm(PasswordChangeForm):
    """Extending Password Change Form
    Overriding help_text

    """
    new_password1 = PasswordField()
    new_password2 = PasswordConfirmationField(confirm_with="new_password1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # help_text = "<ul>" \
        #             "<li>Your password can't be too similar to " \
        #             "your other personal information</li>" \
        #             "<li>Your password must contain " \
        #             "at least 14 characters</li>" \
        #             "<li>Your password can't be a " \
        #             "commonly used password</li>" \
        #             "<li>Your password can't be " \
        #             "entirely numeric</li>" \
        #             "<li>Your password must not be " \
        #             "the same as the current password</li>" \
        #             "<li>Your password must use of " \
        #             "both uppercase and lowercase letters</li>" \
        #             "<li>Your password must include " \
        #             "of one or more numerical digits</li>" \
        #             "<li>Your password must include " \
        #             "of special characters, such as @, #, $</li>" \
        #             "</ul>"
        # self.fields['new_password1'].help_text = help_text

    class Meta:
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]

    def clean(self):
        """Clean is first in order not to have not matched
        error if other validation fails
        """
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError('Your new password and '
                                        'confirmation do not match')

    def clean_new_password1(self):
        """Validating the Password1 Field"""
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if check_password(new_password1, self.user.password):
            raise forms.ValidationError('Your password must not be '
                                        'the same as the current password')

        characters = set(new_password1)

        lower = any(letter.islower() for letter in characters)
        upper = any(letter.isupper() for letter in characters)
        digit = any(letter.isdigit() for letter in characters)

        if not upper:
            raise forms.ValidationError('Your password must use of '
                                        'both uppercase and lowercase letters')

        if not lower:
            raise forms.ValidationError('Your password must use of '
                                        'both uppercase and lowercase letters')

        if not digit:
            raise forms.ValidationError('Your password must include '
                                        'of one or more numerical digits')

        special_characters = ["@", "#", "$"]
        check = False
        for character in special_characters:
            if character in new_password1:
                check = True

        if not check:
            raise forms.ValidationError('Your password must include of '
                                        'special characters, such as @, #, $')

        first_name = self.user.profile.first_name.lower()
        last_name = self.user.profile.last_name.lower()

        if first_name in new_password1.lower():
            raise forms.ValidationError('Your password cannot be too '
                                        'similar to your other personal '
                                        'information')

        if last_name in new_password1.lower():
            raise forms.ValidationError('Your password cannot be too '
                                        'similar to your other personal '
                                        'information')

        return new_password1
