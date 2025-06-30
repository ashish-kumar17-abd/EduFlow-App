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

        # Apply Bootstrap classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Subject queryset dynamic
        course = self.data.get('course') or (self.instance.course if self.instance.pk else None)
        semester = self.data.get('semester') or (self.instance.semester if self.instance.pk else None)

        if course and semester:
            try:
                semester = int(semester)
                self.fields['subject'].queryset = Subject.objects.filter(course__iexact=course, semester=semester)
            except (ValueError, TypeError):
                self.fields['subject'].queryset = Subject.objects.none()
        elif self.instance.pk:
            self.fields['subject'].queryset = Subject.objects.filter(course__iexact=self.instance.course, semester=self.instance.semester)
        else:
            self.fields['subject'].queryset = Subject.objects.none()

        # Generate time slots
        def generate_slots():
            start = datetime.datetime.strptime("09:40", "%H:%M")
            slots = []
            for i in range(6):
                end = start + datetime.timedelta(minutes=40)
                slots.append((start.time(), end.time()))
                start = end
                if i == 3:
                    start += datetime.timedelta(hours=1)  # Lunch break
            return slots

        time_choices = [(slot[0].strftime("%H:%M"), slot[0].strftime("%I:%M %p")) for slot in generate_slots()]
        self.fields['start_time'].widget = forms.Select(choices=time_choices)
        self.fields['end_time'].widget = forms.Select(choices=time_choices)
