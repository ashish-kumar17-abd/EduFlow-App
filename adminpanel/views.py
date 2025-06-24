from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render,redirect
from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject
from attendance.models import Attendance
from datetime import date
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib import messages

# ✅ Only allow superusers (admins)
def is_superuser(user):
    return user.is_superuser

# ✅ Admin Dashboard View
@user_passes_test(is_superuser)
def admin_dashboard(request):
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()
    subjects_count = Subject.objects.count()
    attendance_today = Attendance.objects.filter(date=date.today()).count()

    context = {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'subjects_count': subjects_count,
        'attendance_today': attendance_today,
    }

    return render(request, 'adminpanel/dashboard.html', context)

# ✅ Course-wise & Semester-wise Student Distribution
@user_passes_test(is_superuser)
def student_distribution_view(request):
    distribution = (
        Student.objects
        .values('course', 'semester')
        .annotate(count=Count('id'))
        .order_by('course', 'semester')
    )

    return render(request, 'adminpanel/student_distribution.html', {
        'distribution': distribution
    })


@user_passes_test(is_superuser)
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('admin_student_list')  # Or your custom listing URL

@user_passes_test(is_superuser)
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    messages.success(request, "Teacher deleted successfully.")
    return redirect('admin_teacher_list')  # Or your custom listing URL


@user_passes_test(is_superuser)
def student_filter_view(request):
    course = request.GET.get('course')
    semester = request.GET.get('semester')
    courses = Student.objects.values_list('course', flat=True).distinct()
    students = []

    if course and semester:
        students = Student.objects.filter(course=course, semester=semester)

    context = {
        'courses': courses,
        'selected_course': course,
        'selected_semester': semester,
        'students': students,
        'semesters': range(1, 9),  # 🔥 sending this to template
    }
    return render(request, 'adminpanel/student_filter.html', context)
