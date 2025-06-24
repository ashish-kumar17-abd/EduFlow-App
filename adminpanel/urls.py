from django.urls import path
from . import views

# adminpanel/urls.py

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('teachers/delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('distribution/', views.student_distribution_view, name='student_distribution'),
    path('students/filter/', views.student_filter_view, name='student_filter'),

]

