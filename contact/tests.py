from django.test import TestCase
from django.utils import timezone

from contact.models import Contact
from contact.forms import ContactForm

from contact import forms
from rebar.testing import flatten_to_dict


# class ContactTests(TestCase):
#     """Contact model tests."""
#
#     def test_str(self):
#
#         contact = Contact(sender='test@contact.ru',
#
#                           )
#
#         self.assertEquals(
#             str(contact),
#             'test@contact.ru',
#         )
#

class ContactTestsCase(TestCase):
    """ContactForm tests."""

    def test_valid_form(self):
        name = 'A new name'
        sender = 'test@test.ru'
        message = 'Some test message'
        obj = Contact.objects.create(name=name, sender=sender, message=message, created=timezone.now())
        data={'name': obj.name, 'sender': obj.sender,'message': obj.message, 'created': obj.created}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), obj.name)
        self.assertNotEqual(form.cleaned_data.get('message'), 'Another message')

    def test_invalid_form(self):
        name = 'A new name'
        sender = 'test@test.ru'
        message = 'Some test message'
        obj = Contact.objects.create(name=name, sender=sender, message=message, created=timezone.now())
        data = {'name': obj.name, 'sender': obj.sender, 'message': "", 'created': obj.created}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

