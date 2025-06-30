from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib import messages
from collections import defaultdict
from .models import Timetable
from .forms import TimetableForm
from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject


@login_required
def teacher_timetable(request):
    teacher = Teacher.objects.get(user=request.user)
    subjects = Subject.objects.filter(teacher=teacher)
    timetable = Timetable.objects.filter(subject__in=subjects).order_by('day', 'start_time')

    grouped_by_day = defaultdict(list)
    for entry in timetable:
        grouped_by_day[entry.day].append(entry)

    return render(request, 'timetable/teacher_timetable.html', {
        'teacher_name': teacher.full_name,
        'grouped_by_day': dict(grouped_by_day),
    })


@staff_member_required
def admin_timetable_list(request):
    all_entries = Timetable.objects.all().order_by('day', 'start_time')
    time_slots = sorted(set((t.start_time, t.end_time) for t in all_entries))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timetable_grid = defaultdict(dict)
    for t in all_entries:
        slot = (t.start_time, t.end_time)
        timetable_grid[t.day][slot] = t
    return render(request, 'timetable/admin_timetable_list.html', {
        'time_slots': time_slots,
        'days': days,
        'timetable_grid': timetable_grid,
    })

@staff_member_required
def add_timetable(request):
    form = TimetableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Timetable added.")
        return redirect('admin_timetable_list')
    return render(request, 'timetable/admin_timetable_form.html', {'form': form})


@staff_member_required
def timetable_courses(request):
    courses = Timetable.objects.values_list('course', flat=True).distinct()
    return render(request, 'timetable/admin_course_list.html', {'courses': courses})

@staff_member_required
def timetable_semesters(request, course):
    semesters = Timetable.objects.filter(course__iexact=course).values_list('semester', flat=True).distinct()
    return render(request, 'timetable/admin_semester_list.html', {
        'course': course,
        'semesters': semesters,
    })

from django.db.models.functions import Lower

@staff_member_required
def timetable_detail(request, course, semester):
    entries = Timetable.objects.filter(course__iexact=course, semester=semester).order_by('day', 'start_time')
    time_slots = sorted(set((t.start_time, t.end_time) for t in entries))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    timetable_grid = defaultdict(dict)
    for t in entries:
        slot = (t.start_time, t.end_time)
        timetable_grid[t.day][slot] = t

    return render(request, 'timetable/admin_timetable_list.html', {
        'time_slots': time_slots,
        'days': days,
        'timetable_grid': timetable_grid,
        'course': course,
        'semester': semester,
    })




@staff_member_required
def edit_timetable(request, pk):
    timetable = Timetable.objects.get(pk=pk)
    form = TimetableForm(request.POST or None, instance=timetable)
    if form.is_valid():
        form.save()
        messages.success(request, "Timetable updated.")
        return redirect('admin_timetable_detail', course=timetable.course, semester=timetable.semester)
    return render(request, 'timetable/admin_timetable_form.html', {'form': form})


@staff_member_required
def delete_timetable(request, pk):
    timetable = Timetable.objects.get(pk=pk)
    course = timetable.course
    semester = timetable.semester
    timetable.delete()
    messages.success(request, "Timetable deleted.")
    return redirect('admin_timetable_detail', course=course, semester=semester)


@login_required
def student_timetable(request):
    student = Student.objects.get(user=request.user)

    subjects = Subject.objects.filter(course__iexact=student.course, semester=student.semester)
    timetable = Timetable.objects.filter(subject__in=subjects).order_by('day', 'start_time')

    grouped_by_day = defaultdict(list)
    for entry in timetable:
        grouped_by_day[entry.day].append(entry)

    return render(request, 'timetable/student_timetable.html', {
        'grouped_by_day': dict(grouped_by_day),
        'course': student.course,
        'semester': student.semester,
    })


@staff_member_required
def get_subjects_ajax(request):
    course = request.GET.get('course')
    semester = request.GET.get('semester')
    if course and semester:
        try:
            semester = int(semester)
            subjects = Subject.objects.filter(course__iexact=course, semester=semester).values('id', 'name')
            return JsonResponse(list(subjects), safe=False)
        except:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)







