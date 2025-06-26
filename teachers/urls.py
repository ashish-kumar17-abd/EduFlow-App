from django.urls import path
from . import views

urlpatterns = [
    path('complete-profile/', views.complete_teacher_profile, name='complete_teacher_profile'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # ✅ THIS LINE
    path('edit-profile/', views.edit_teacher_profile, name='edit_teacher_profile'),
    # path('admin/teachers/', views.admin_teacher_list, name='admin_teacher_list'),
    path('admin/teachers/', views.admin_teacher_list, name='admin_teacher_list'),

]
