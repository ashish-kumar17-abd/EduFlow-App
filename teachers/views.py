from django.shortcuts import render, redirect
from .forms import TeacherForm
from .models import Teacher
from subjects.models import Subject
from django.contrib.auth.decorators import login_required

@login_required
def complete_teacher_profile(request):
    if Teacher.objects.filter(user=request.user).exists():
        return redirect('teacher_dashboard')  # Already created

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherForm()

    return render(request, 'teachers/complete_profile.html', {'form': form})



@login_required
def edit_teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_profile.html', {'form': form})


@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        subjects = Subject.objects.filter(teacher=teacher)
    except Teacher.DoesNotExist:
        teacher = None
        subjects = []

    return render(request, 'dashboard/teacher.html', {
        'teacher': teacher,
        'subjects': subjects,
    })