from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from . import models


class UserProfileForm(forms.ModelForm):
    email2 = forms.EmailField(label='Confirm Email')

    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
            'bio',
            'avatar'
        ]
    field_order = ['first_name', 'last_name', 'email', 'email2', 'birthday',
                   'bio', 'avatar']

    def clean_email2(self):
        emai2 = self.cleaned_data['email2']
        if self.cleaned_data['email'] != emai2:
            raise forms.ValidationError(
                'Emails do not match!'
            )
        return emai2

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                'bio must be at least 10 characters long'
            )
        return bio


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super(CustomPasswordChangeForm, self).clean()
        new_password = cleaned_data.get('new_password1')
        old_password = cleaned_data.get('old_password')
        if old_password == new_password:
            raise forms.ValidationError(
                'new password cannot be the same as old password.'
            )
        user = self.user
        if user.username.lower() in new_password.lower():
            raise forms.ValidationError(
                'password cannot contain username,'
            )
        try:
            profile = models.UserProfile.objects.get(user=self.user)
        except models.UserProfile.DoesNotExist:
            pass
        else:
            if (profile.first_name.lower() in new_password.lower()) or (
                        profile.last_name.lower() in new_password.lower()):
                raise forms.ValidationError(
                    'password cannot contain first name or last name.'
                )
