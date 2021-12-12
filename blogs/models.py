from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000)
    date = models.DateTimeField('Date')
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
