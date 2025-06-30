from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_timetable, name='student_timetable'),
    path('teacher/', views.teacher_timetable, name='teacher_timetable'),

    path('admin/list/', views.admin_timetable_list, name='admin_timetable_list'),
    path('admin/add/', views.add_timetable, name='add_timetable'),
    path('get-subjects/', views.get_subjects_ajax, name='get_subjects_ajax'),
    path('admin/<int:pk>/edit/', views.edit_timetable, name='edit_timetable'),
    path('admin/<int:pk>/delete/', views.delete_timetable, name='delete_timetable'),

    path('get-subjects/', views.get_subjects_ajax, name='get_subjects_ajax'),
    path('admin/courses/', views.timetable_courses, name='admin_timetable_courses'),
    path('admin/<str:course>/', views.timetable_semesters, name='admin_timetable_semesters'),
    path('admin/<str:course>/<int:semester>/', views.timetable_detail, name='admin_timetable_detail'),


]
