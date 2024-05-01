from django import forms
from home.models import Notes, User
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = (
            "title",
            "content",
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class ShareNotesForm(forms.Form):
    shareid = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "shareid" in self.fields:
            self.fields["shareid"].widget.attrs["readonly"] = True
