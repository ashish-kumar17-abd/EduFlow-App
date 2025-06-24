from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import Profile
from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject

# -------------------------
# Signup View
# -------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data['role']
            user.profile.role = role
            user.profile.save()

            if role == 'student':
                login(request, user)
                return redirect('complete_student_profile')
            elif role == 'teacher':
                login(request, user)
                return redirect('complete_teacher_profile')

            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})


# -------------------------
# Login View (Updated)
# -------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # ✅ Superuser redirect
                if user.is_superuser:
                    return redirect('admin_dashboard')

                # ✅ Redirect based on profile role
                if hasattr(user, 'profile'):
                    if user.profile.role == 'student':
                        if not Student.objects.filter(user=user).exists():
                            return redirect('complete_student_profile')
                        return redirect('student_dashboard')

                    elif user.profile.role == 'teacher':
                        if not Teacher.objects.filter(user=user).exists():
                            return redirect('complete_teacher_profile')
                        return redirect('teacher_dashboard')

                return redirect('home')  # fallback
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


# -------------------------
# Logout View
# -------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------
# Student Dashboard
# -------------------------
@login_required
def student_dashboard(request):
    try:
        student_profile = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('complete_student_profile')
    return render(request, 'dashboard/student.html', {'student': student_profile})


# -------------------------
# Teacher Dashboard
# -------------------------
@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = None
    return render(request, 'dashboard/teacher.html', {'teacher': teacher})


# -------------------------
# Role-based Redirect
# -------------------------
@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    if hasattr(user, 'profile'):
        if user.profile.role == 'student':
            return redirect('student_dashboard')
        elif user.profile.role == 'teacher':
            return redirect('teacher_dashboard')
    return redirect('home')
