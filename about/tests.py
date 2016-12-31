from django.test import TestCase
from .models import SignUp
from .forms import SignUpForm
from django.utils import timezone


class SignUpTestsCase(TestCase):
    """SignUpForm  tests."""

    def test_valid_form(self):
        email = 'test@test.ru'
        obj = SignUp.objects.create(email=email, timestamp=timezone.now())
        data = {'email': obj.email, 'timestamp': obj.timestamp}
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('email'), obj.email)
        self.assertNotEqual(form.cleaned_data.get('email'), 'another@email.ru')

    def test_invalid_form(self):
        email = 'test@test.ru'
        obj = SignUp.objects.create(email=email, timestamp=timezone.now())
        data = {'email': obj.email, 'timestamp': obj.timestamp}
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)



