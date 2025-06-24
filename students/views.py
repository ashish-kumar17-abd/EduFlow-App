# students/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentForm
from attendance.models import Attendance
from subjects.models import Subject
from collections import defaultdict

# Check if user is admin
def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

# Admin view to list all students
@login_required
@user_passes_test(is_admin)
def admin_student_list(request):
    students = Student.objects.all()
    return render(request, 'students/admin_student_list.html', {'students': students})

# Admin or student can view individual student details
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

# Student profile completion
@login_required
def complete_student_profile(request):
    if Student.objects.filter(user=request.user).exists():
        return redirect('student_dashboard')  # already filled

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect('student_dashboard')
    else:
        form = StudentForm()

    return render(request, 'students/complete_profile.html', {'form': form})

# Student profile editing
@login_required
def edit_student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('complete_student_profile')  # redirect if profile not created

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_profile.html', {'form': form})

# Student dashboard with subject-wise attendance summary
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('complete_student_profile')

    attendances = Attendance.objects.filter(student=student).order_by('date')

    # Group attendance by subject
    subject_data = defaultdict(lambda: {'dates': {}, 'present': 0, 'total': 0, 'percentage': 0})

    for att in attendances:
        sub = att.subject
        subject_data[sub]['dates'][att.date] = att.status
        subject_data[sub]['total'] += 1
        if att.status == 'Present':
            subject_data[sub]['present'] += 1

    for sub, data in subject_data.items():
        data['percentage'] = round((data['present'] / data['total']) * 100, 1) if data['total'] else 0

    return render(request, 'dashboard/student.html', {
        'student': student,
        'subject_data': subject_data
    })

# View to show subject-wise attendance detail

@login_required
def student_attendance_view(request):
    student = Student.objects.get(user=request.user)
    attendances = Attendance.objects.filter(student=student).select_related('subject').order_by('subject', 'date')

    subject_data = defaultdict(lambda: {
        'subject': None,
        'records': [],
        'present': 0,
        'total': 0,
        'percentage': 0
    })

    for att in attendances:
        sub_id = att.subject.id
        subject_data[sub_id]['subject'] = att.subject
        subject_data[sub_id]['records'].append({'date': att.date, 'status': att.status})
        subject_data[sub_id]['total'] += 1
        if att.status == 'Present':
            subject_data[sub_id]['present'] += 1

    for data in subject_data.values():
        total = data['total']
        present = data['present']
        data['percentage'] = round((present / total) * 100, 1) if total else 0

    return render(request, 'students/my_attendance.html', {
        'subject_data': subject_data.values()
    })