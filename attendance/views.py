from django.shortcuts import render, redirect
from students.models import Student
from subjects.models import Subject
from .models import Attendance
from teachers.models import Teacher
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# ================== MARK ATTENDANCE ==================

@login_required
def mark_attendance(request):
    teacher = Teacher.objects.get(user=request.user)
    subjects = Subject.objects.filter(teacher=teacher)

    students = []
    selected_subject = None
    selected_date = timezone.now().date()
    attendance_map = {}

    if request.method in ['POST', 'GET']:
        subject_id = request.POST.get('subject') or request.GET.get('subject')
        date_str = request.POST.get('date') or request.GET.get('date')

        # Date parse
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except:
                selected_date = timezone.now().date()

        # Subject select
        if subject_id:
            try:
                selected_subject = Subject.objects.get(id=subject_id)
                students = Student.objects.filter(
                    semester=selected_subject.semester,
                    course__iexact=(selected_subject.course or '').strip()
                )

                # ✅ If Attendance is being marked (actual submission)
                if request.method == 'POST' and any(k.startswith('status_') for k in request.POST.keys()):
                    Attendance.objects.filter(subject=selected_subject, date=selected_date).delete()

                    for student in students:
                        status = request.POST.get(f'status_{student.id}')
                        if status:
                            Attendance.objects.create(
                                student=student,
                                subject=selected_subject,
                                date=selected_date,
                                status=status,
                                marked_by=teacher,
                            )

                    messages.success(request, "Attendance marked successfully!")
                    return redirect('mark_attendance')

            except Subject.DoesNotExist:
                selected_subject = None

    return render(request, 'attendance/mark_attendance.html', {
        'subjects': subjects,
        'students': students,
        'selected_subject': selected_subject,
        'selected_date': selected_date,
        'today': timezone.now().date()
    })



# ================== ATTENDANCE REPORT ==================

@login_required
def attendance_report(request):
    selected_course = request.GET.get('course', '').strip()
    selected_semester = request.GET.get('semester', '').strip()
    selected_subject_id = request.GET.get('subject')

    subjects = Subject.objects.all()
    if selected_course:
        subjects = subjects.filter(course__iexact=selected_course)
    if selected_semester:
        subjects = subjects.filter(semester=selected_semester)

    students = []
    attendance_dates = []
    attendance_data = defaultdict(dict)
    summary_stats = {}

    if selected_subject_id:
        try:
            subject = Subject.objects.get(id=selected_subject_id)
            students = Student.objects.filter(
                course__iexact=subject.course.strip(),
                semester=subject.semester
            )

            attendances = Attendance.objects.filter(subject=subject).order_by('date')
            attendance_dates = sorted(set(att.date for att in attendances))

            for att in attendances:
                attendance_data[att.student.id][att.date] = att.status

            for student in students:
                sid = student.id
                present = sum(1 for d in attendance_dates if attendance_data[sid].get(d) == 'Present')
                total = len(attendance_dates)
                percentage = round((present / total) * 100, 1) if total else 0

                summary_stats[sid] = {
                    'present': present,
                    'total': total,
                    'percentage': percentage
                }

        except Subject.DoesNotExist:
            pass

    return render(request, 'attendance/admin_report.html', {
        'subjects': subjects,
        'selected_course': selected_course,
        'selected_semester': selected_semester,
        'selected_subject_id': selected_subject_id,
        'students': students,
        'attendance_dates': attendance_dates,
        'attendance_data': attendance_data,
        'summary_stats': summary_stats
    })


@login_required
def unmark_attendance(request):
    teacher = Teacher.objects.get(user=request.user)

    student_id = request.GET.get('student')
    subject_id = request.GET.get('subject')
    date_str = request.GET.get('date')

    if student_id and subject_id and date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            attendance = Attendance.objects.get(
                student_id=student_id,
                subject_id=subject_id,
                date=date,
                marked_by=teacher
            )
            attendance.delete()
            messages.success(request, "Attendance entry deleted successfully.")
        except Attendance.DoesNotExist:
            messages.error(request, "Attendance entry not found.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return HttpResponseRedirect(reverse('mark_attendance'))


@login_required
def edit_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')
        date_str = request.POST.get('date')
        status = request.POST.get('status')

        if student_id and subject_id and date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            try:
                attendance = Attendance.objects.get(
                    student_id=student_id,
                    subject_id=subject_id,
                    date=date
                )
                if status:
                    attendance.status = status
                    attendance.save()
                else:
                    attendance.delete()
            except Attendance.DoesNotExist:
                if status:
                    Attendance.objects.create(
                        student_id=student_id,
                        subject_id=subject_id,
                        date=date,
                        status=status,
                        marked_by=Teacher.objects.get(user=request.user)
                    )

    return redirect('attendance_report')
