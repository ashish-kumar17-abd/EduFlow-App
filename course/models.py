from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    duration = models.PositiveIntegerField(help_text="In years")
    total_semesters = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = ('course', 'number')  # prevent duplicate semesters per course
        ordering = ['number']

    def __str__(self):
        return f"{self.course.code} - Semester {self.number}"
