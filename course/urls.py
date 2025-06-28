from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/semesters/', views.view_semesters, name='view_semesters'),
    # courses/urls.py
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),
    # path('<int:course_id>/delete/', views.delete_course, name='delete_course'),


]
