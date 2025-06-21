
# Create your views here.
# students/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,get_object_or_404,redirect
from .models import Student
from .forms import StudentForm

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
@user_passes_test(is_admin)
def admin_student_list(request):
    students = Student.objects.all()
    return render(request, 'students/admin_student_list.html', {'students': students})



def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


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


@login_required
def student_dashboard(request):
    try:
        student_profile = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student_profile = None

    return render(request, 'dashboard/student.html', {'student': student_profile})
