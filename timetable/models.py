from django.db import models
from subjects.models import Subject
from teachers.models import Teacher

class Timetable(models.Model):
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.course} - Sem {self.semester} - {self.subject.name} ({self.day})"


from django import forms
from .models import Timetable
from subjects.models import Subject
import datetime

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'semester', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Filter subjects
        self.fields['subject'].queryset = Subject.objects.none()
        course = self.data.get('course') or (self.instance.course if self.instance.pk else None)
        semester = self.data.get('semester') or (self.instance.semester if self.instance.pk else None)

        if course and semester:
            try:
                semester = int(semester)
                self.fields['subject'].queryset = Subject.objects.filter(course__iexact=course, semester=semester)
            except:
                pass

        # Generate fixed 40-min time slots (9:40 start, 4 classes, 1 hour lunch, 2 classes)
        def generate_slots():
            start = datetime.datetime.strptime("09:40", "%H:%M")
            slots = []
            for i in range(6):
                end = start + datetime.timedelta(minutes=40)
                slots.append((start.time(), end.time()))
                start = end
                if i == 3:
                    start += datetime.timedelta(hours=1)
            return slots

        time_choices = [(slot[0].strftime("%H:%M"), slot[0].strftime("%I:%M %p")) for slot in generate_slots()]
        self.fields['start_time'].widget = forms.Select(choices=time_choices)
        self.fields['end_time'].widget = forms.Select(choices=time_choices)
