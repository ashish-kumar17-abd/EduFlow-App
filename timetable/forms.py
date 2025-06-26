from django import forms
from .models import Timetable
from subjects.models import Subject

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'semester', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.none()
        course = self.data.get('course') or (self.instance.course if self.instance.pk else None)
        semester = self.data.get('semester') or (self.instance.semester if self.instance.pk else None)

        if course and semester:
            try:
                semester = int(semester)
                self.fields['subject'].queryset = Subject.objects.filter(course__iexact=course, semester=semester)
            except:
                pass
