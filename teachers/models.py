from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='teacher_images/', blank=True, null=True)

    def __str__(self):
        return self.full_name
