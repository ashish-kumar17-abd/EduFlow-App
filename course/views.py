from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Semester
from .forms import CourseForm
from django.contrib import messages

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/add_course.html', {'form': form})


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/edit_course.html', {'form': form, 'course': course})


def view_semesters(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    semesters = Semester.objects.filter(course=course)
    return render(request, 'course/semesters.html', {'course': course, 'semesters': semesters})


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f"Course '{course.name}' deleted successfully.")
        return redirect('course_list')
    return render(request, 'course/delete_course_confirm.html', {'course': course})