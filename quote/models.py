from django.db import models

# Create your models here.
class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    quote = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)