from django.contrib import admin
from .models import Timetable

admin.site.register(Timetable)


from django.shortcuts import render
from .models import Timetable

def timetable_courses(request):
    courses = Timetable.objects.values_list('course', flat=True).distinct()
    return render(request, 'timetable/admin_course_list.html', {'courses': courses})
