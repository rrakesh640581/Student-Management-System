from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='students'
)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name