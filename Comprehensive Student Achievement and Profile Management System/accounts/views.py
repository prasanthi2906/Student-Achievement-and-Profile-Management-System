from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from students.models import Student
from students.forms import StudentDocumentUploadForm, StudentAchievementForm
from documents.models import Document
from achievements.models import Achievement

def custom_logout(request):
    """Custom logout view that works for both admin and frontend"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def student_login(request):
    """Student login view using registration number and temporary password"""
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number')
        password = request.POST.get('password')
        
        # Find student by registration number
        try:
            student = Student.objects.get(registration_number=registration_number)
            # Check if student has credentials
            if hasattr(student, 'credential'):
                # Allow login with temporary password regardless of activation status
                # This enables students to login with their initial credentials
                if student.credential.temporary_password == password:
                    # Create session for student
                    request.session['student_id'] = student.id
                    request.session['is_student'] = True
                    messages.success(request, f'Welcome back, {student.full_name}!')
                    
                    # Activate account on first login
                    if not student.credential.is_active:
                        from accounts.utils import activate_student_account
                        activate_student_account(student)
                        messages.info(request, 'Your account has been activated!')
                    
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid password')
            else:
                messages.error(request, 'Account not found or credentials not generated yet')
        except Student.DoesNotExist:
            messages.error(request, 'Student not found')
    
    return render(request, 'registration/student_login.html')

def student_dashboard(request):
    """Student personal dashboard"""
    # Check if student is logged in
    if not request.session.get('is_student'):
        messages.error(request, 'Please login as a student')
        return redirect('student_login')
    
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    
    context = {
        'student': student,
        'documents': student.documents.all(),
        'achievements': student.achievements.all(),
    }
    return render(request, 'students/dashboard.html', context)

def student_document_upload(request):
    """Allow students to upload their own documents"""
    # Check if user is student (using custom session authentication)
    if not request.session.get('is_student'):
        messages.error(request, 'Please login as a student')
        return redirect('student_login')
    
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentDocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = student
            document.verified = False  # Default to pending verification
            document.save()
            messages.success(request, 'Document uploaded successfully! Awaiting admin verification.')
            return redirect('student_dashboard')
    else:
        form = StudentDocumentUploadForm()
    
    return render(request, 'students/upload_document.html', {'form': form})

def student_achievement_submit(request):
    """Allow students to submit their own achievements"""
    # Check if user is student
    if not request.session.get('is_student'):
        messages.error(request, 'Please login as a student')
        return redirect('student_login')
    
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentAchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.student = student
            achievement.status = 'SUBMITTED'  # Default to submitted status
            achievement.save()
            messages.success(request, 'Achievement submitted successfully! Awaiting admin approval.')
            return redirect('student_dashboard')
    else:
        form = StudentAchievementForm()
    
    return render(request, 'students/submit_achievement.html', {'form': form})

def student_logout(request):
    """Student logout"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')