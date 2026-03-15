import os
import django
from datetime import date

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Student
from accounts.models import RegistrationRequest, StudentCredential
from students.forms import StudentSelfRegistrationForm

print("=== WORKFLOW VERIFICATION ===")
print()

# Show current state
print("CURRENT STATE:")
print(f"Students: {Student.objects.count()}")
print(f"Registration Requests: {RegistrationRequest.objects.count()}")
print(f"Student Credentials: {StudentCredential.objects.count()}")
print()

# Test registration
print("--- TESTING REGISTRATION ---")
test_data = {
    'first_name': 'Bob',
    'last_name': 'Wilson',
    'email': 'bob.wilson@college.edu',
    'phone': '8877665544',
    'date_of_birth': '2001-03-20',
    'enrollment_date': '2024-08-20',
    'address': '789 Pine Street, Hyderabad',
    'admission_category': 'ECET',
    'program': 'Electrical Engineering'
}

print("Creating student via form...")
form = StudentSelfRegistrationForm(data=test_data)
if form.is_valid():
    student = form.save()
    print(f"SUCCESS: Student created - {student.full_name} ({student.registration_number})")
    
    # Create RegistrationRequest (simulating the view logic)
    registration_request = RegistrationRequest.objects.create(
        student=student,
        status='PENDING'
    )
    print(f"SUCCESS: RegistrationRequest created - ID: {registration_request.id}, Status: {registration_request.status}")
else:
    print("ERROR: Form validation failed")
    for field, errors in form.errors.items():
        print(f"  {field}: {errors}")

print()
print("FINAL COUNTS:")
print(f"Students: {Student.objects.count()}")
print(f"Registration Requests: {RegistrationRequest.objects.count()}")
print(f"Student Credentials: {StudentCredential.objects.count()}")

print()
print("All Registration Requests:")
for req in RegistrationRequest.objects.all().order_by('-submitted_at'):
    has_credential = hasattr(req.student, 'credential')
    print(f"- {req.student.full_name} ({req.student.registration_number}): {req.status} - Credential: {has_credential}")