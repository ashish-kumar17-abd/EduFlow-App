# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin/students/', views.admin_student_list, name='admin_student_list'),
    path('admin/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('complete-profile/', views.complete_student_profile, name='complete_student_profile'),
    path('edit-profile/', views.edit_student_profile, name='edit_student_profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('my-attendance/', views.student_attendance_view, name='student_attendance'),

]
