from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import Profile
from students.models import Student  # For fetching student profile

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
                login(request, user)  # auto login
                return redirect('complete_student_profile')

            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})



# -------------------------
# Login View
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

                # Redirect based on role
                if hasattr(user, 'profile'):
                    if user.profile.role == 'student':
                        return redirect('student_dashboard')
                    elif user.profile.role == 'teacher':
                        return redirect('teacher_dashboard')
                return redirect('home')
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
        student_profile = None
    return render(request, 'dashboard/student.html', {'student': student_profile})


# -------------------------
# Teacher Dashboard
# -------------------------
@login_required
def teacher_dashboard(request):
    return render(request, 'authentication/teacher.html')


# -------------------------
# Role-based Redirect (optional)
# -------------------------
@login_required
def role_based_redirect(request):
    user = request.user
    if hasattr(user, 'profile'):
        if user.profile.role == 'student':
            return redirect('student_dashboard')
        elif user.profile.role == 'teacher':
            return redirect('teacher_dashboard')
    return redirect('home')
