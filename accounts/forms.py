from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name","username","email","role","school","bio","profile_photo", ]

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","role","school","bio","profile_photo","is_active", ]
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","school","role","profile_photo","bio","password1","password2",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["role"].widget.attrs["class"] = "form-select"
        