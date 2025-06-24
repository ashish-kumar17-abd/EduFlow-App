from django.urls import path
from . import views

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    
    # ✅ New route to unmark attendance
    path('unmark/', views.unmark_attendance, name='unmark_attendance'),
    path('edit/', views.edit_attendance, name='edit_attendance'),

]
