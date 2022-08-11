from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name}"