from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, OTPForm
from .models import Profile
from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject
import random


# -------------------------
# Helper: OTP Generator
# -------------------------
def generate_otp():
    return str(random.randint(100000, 999999))


# -------------------------
# Signup View with OTP
# -------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save form data to session
            request.session['signup_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'role': form.cleaned_data['role'],
            }

            # Generate OTP
            otp = generate_otp()
            request.session['signup_otp'] = otp

            # Send OTP to email
            send_mail(
                subject='Your EduFlow OTP',
                message=f'Your OTP is: {otp}',
                from_email='ashishkumar8603371492@gmail.com',  # Replace with actual
                recipient_list=[form.cleaned_data['email']],
                fail_silently=False,
            )

            return redirect('verify_otp')
    else:
        form = SignupForm()

    return render(request, 'authentication/signup.html', {'form': form})


# -------------------------
# OTP Verification View
# -------------------------
def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('signup_otp')
            data = request.session.get('signup_data')

            if entered_otp == stored_otp:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                user.profile.role = data['role']
                user.profile.save()
                login(request, user)

                # Clean session
                request.session.pop('signup_otp', None)
                request.session.pop('signup_data', None)

                # Redirect by role
                if data['role'] == 'student':
                    return redirect('complete_student_profile')
                elif data['role'] == 'teacher':
                    return redirect('complete_teacher_profile')
                return redirect('login')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()

    return render(request, 'authentication/verify_otp.html', {'form': form})


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

                if user.is_superuser:
                    return redirect('admin_dashboard')

                if hasattr(user, 'profile'):
                    if user.profile.role == 'student':
                        if not Student.objects.filter(user=user).exists():
                            return redirect('complete_student_profile')
                        return redirect('student_dashboard')

                    elif user.profile.role == 'teacher':
                        if not Teacher.objects.filter(user=user).exists():
                            return redirect('complete_teacher_profile')
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
