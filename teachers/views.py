from django.shortcuts import render, redirect
from .forms import TeacherForm
from .models import Teacher
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher
from .forms import TeacherForm


# ✅ Complete Profile
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


# ✅ Edit Profile
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


# ✅ Teacher Dashboard
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




def admin_teacher_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('login')

    course = request.GET.get('course', '').strip()
    semester = request.GET.get('semester', '').strip()
    subject_id = request.GET.get('subject', '').strip()

    subjects = Subject.objects.all()
    if course:
        subjects = subjects.filter(course__iexact=course)
    if semester:
        subjects = subjects.filter(semester=semester)

    teachers = Teacher.objects.all().distinct()
    if subject_id:
        teachers = teachers.filter(subject__id=subject_id)
    elif course or semester:
        teachers = teachers.filter(subject__in=subjects).distinct()

    # ✅ Important mapping
    teacher_subject_map = {
        teacher.id: Subject.objects.filter(teacher=teacher) for teacher in teachers
    }

    return render(request, 'teachers/admin_teacher_list.html', {
        'teachers': teachers,
        'subjects': Subject.objects.all(),
        'teacher_subject_map': teacher_subject_map,
        'selected_course': course,
        'selected_semester': semester,
        'selected_subject': subject_id,
    })


# ✅ Edit Teacher (Admin Side)
@login_required
def edit_teacher_admin(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully.")
            return redirect('admin_teacher_list')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'teachers/edit_teacher_admin.html', {
        'form': form,
        'teacher': teacher
    })

@login_required
def delete_teacher_admin(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect('admin_teacher_list')

    return render(request, 'teachers/delete_teacher_admin.html', {
        'teacher': teacher
    })