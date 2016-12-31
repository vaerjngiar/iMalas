from django.contrib import admin
from .models import SignUp


class SignUpAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp']

admin.site.register(SignUp, SignUpAdmin)
