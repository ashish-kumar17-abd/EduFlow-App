from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'status', 'date', 'marked_by')
    list_filter = ('date', 'subject', 'status')