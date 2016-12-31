from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    sender = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = ' Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return self.sender
