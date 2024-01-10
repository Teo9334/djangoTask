
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField()
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField()
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title