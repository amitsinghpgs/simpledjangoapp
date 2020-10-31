from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)