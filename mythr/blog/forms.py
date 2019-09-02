from django import forms

from .validators import password_match_validator


# TODO: Add new form validators.
class ProfileEditForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget())
    about = forms.CharField(widget=forms.Textarea())


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget())
    username = forms.CharField(min_length=6)
    email = forms.EmailField()
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        password_match_validator(password1, password2)


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class NewPostForm(forms.Form):
    title = forms.CharField(required=True,
                            max_length=140,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Enter a title. '}))

    content = forms.CharField(required=True,
                              min_length=50,
                              max_length=10000,
                              widget=forms.Textarea(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Express your views. MythrConnect is a safe space :)'}))


class CommentForm(forms.Form):
    content = forms.CharField(required=True,
                              max_length=1000,
                              widget=forms.Textarea(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Say something nice :)'}))
