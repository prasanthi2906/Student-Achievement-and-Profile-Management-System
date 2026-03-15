from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentSelfRegistrationForm
from accounts.temp_models import TemporaryRegistration

def home(request):
    """Home page view"""
    # For public visitors, show limited information
    if request.user.is_authenticated:
        total_students = Student.objects.count()
    else:
        total_students = "Login required to view"
    
    context = {
        'total_students': total_students,
    }
    return render(request, 'home.html', context)

def student_self_register(request):
    """Controlled student self-registration - saves to TemporaryRegistration for admin approval"""
    if request.method == 'POST':
        form = StudentSelfRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save to TemporaryRegistration instead of Student
            from accounts.temp_models import TemporaryRegistration
            
            temp_reg = TemporaryRegistration.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                admission_category=form.cleaned_data['admission_category'],
                program=form.cleaned_data['program'],
                enrollment_date=form.cleaned_data['enrollment_date'],
                status='PENDING'
            )
            
            messages.success(
                request, 
                f'Registration submitted successfully! Your registration is pending administrator approval. '
                f'Once approved, you will receive login credentials.'
            )
            # In a real system, you'd send notification to admin here
            return redirect('home')
    else:
        form = StudentSelfRegistrationForm()
    
    return render(request, 'students/self_register.html', {'form': form})

def student_list(request):
    """List all students - public view with limited information"""
    if request.user.is_authenticated:
        # Authenticated users see basic list
        students = Student.objects.all().order_by('-created_at')
    else:
        # Public visitors see limited information
        students = Student.objects.none()
        messages.info(request, "Please login to view student directory.")
        return redirect('login')
    
    return render(request, 'students/list.html', {'students': students})

@login_required
def register_student(request):
    """Student registration view - requires authentication"""
    if request.method == 'POST':
        form = StudentSelfRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            
            # Auto-approve any pending TemporaryRegistrations with the same email
            pending_temps = TemporaryRegistration.objects.filter(
                email=student.email,
                status='PENDING'
            )
            if pending_temps.exists():
                from django.utils import timezone
                pending_temps.update(
                    status='APPROVED',
                    reviewed_at=timezone.now(),
                    reviewed_by=request.user
                )
            
            messages.success(
                request, 
                f'Student registered successfully! Registration Number: {student.registration_number}'
            )
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentSelfRegistrationForm()
    
    return render(request, 'students/register.html', {'form': form})

def student_detail(request, pk):
    """View student details - requires authentication"""
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view student details.")
        return redirect('login')
        
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})

@login_required
def student_update(request, pk):
    """Update student information - requires authentication"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentSelfRegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentSelfRegistrationForm(instance=student)
    
    return render(request, 'students/update.html', {'form': form, 'student': student})

@login_required
def student_delete(request, pk):
    """Delete student - requires authentication"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        registration_number = student.registration_number
        student.delete()
        messages.success(request, f'Student {registration_number} deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'students/delete.html', {'student': student})
