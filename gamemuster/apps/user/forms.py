from django import forms

from .models import CustomUser
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth_date')

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=16, required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=16, required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if str(cleaned_data['password']) != str(cleaned_data['password_confirm']):
            self.add_error('password_confirm', 'Passwords don\'t match')
        return cleaned_data
