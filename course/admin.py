from django.contrib import admin
from .models import Course, Semester

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration', 'total_semesters')
    search_fields = ('name', 'code')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'title')
    list_filter = ('course',)
    ordering = ('course', 'number')
