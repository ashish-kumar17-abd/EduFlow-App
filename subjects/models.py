from django.db import models
from teachers.models import Teacher  # once teacher app is created

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
