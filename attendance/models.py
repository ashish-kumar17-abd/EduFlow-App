# attendance/models.py

from django.db import models
from teachers.models import Teacher
from students.models import Student
from subjects.models import Subject

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))
    marked_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name} - {self.date} - {self.status}"


