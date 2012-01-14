from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    email=forms.EmailField(label='Email')
    first_name=forms.CharField(min_length=1, max_length=30, label='First Name', )
    last_name=forms.CharField(min_length=1, max_length=30, label='Last Name', )
    password1=forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password')
    password2=forms.CharField(widget=forms.PasswordInput(render_value=False), label='Confirm Password')
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Your passwords did not match')
        return self.cleaned_data
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('This email address is already being used. Please provide a different email address.')
        return self.cleaned_data['email']