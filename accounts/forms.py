from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name","username","email","role","school","bio","profile_photo", ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "role", "school", "bio", "profile_photo", "is_active"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            elif field_name == "role":
                field.widget.attrs["class"] = "form-select"
            elif field_name == "profile_photo":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-control"

class PhotoProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["profile_photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_photo"].widget.attrs["class"] = "form-control"
        
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","school","role","profile_photo","bio","password1","password2",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["role"].widget.attrs["class"] = "form-select"
        