from django import forms
from contact.models import Contact
from about.models import SignUp


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'sender', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Type your name'}),
            'sender': forms.TextInput(attrs={'placeholder': 'Type your email'}),

        }


class SignUpForm(forms.ModelForm):

    class Meta:
        model = SignUp
        fields = ['email']

