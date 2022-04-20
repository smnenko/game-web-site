from django import forms

from .models import Avatar


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('avatar',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=16, required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=16, required=True, widget=forms.TextInput())
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    first_name = forms.CharField(max_length=64, required=True, widget=forms.TextInput())
    last_name = forms.CharField(max_length=64, required=True, widget=forms.TextInput())
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if str(cleaned_data['password']) != str(cleaned_data['password_confirm']):
            self.add_error('password_confirm', 'Passwords don\'t match')
        return cleaned_data
