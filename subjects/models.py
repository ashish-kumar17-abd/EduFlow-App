# subjects/models.py
from teachers.models import Teacher  # make sure this is imported
# 👇 Add this import at the top of the file
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 important

    def __str__(self):
        return self.name
