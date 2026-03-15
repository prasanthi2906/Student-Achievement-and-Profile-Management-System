import os
import django
from datetime import date

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Student
from accounts.models import RegistrationRequest
from students.forms import StudentSelfRegistrationForm

# Test data
test_data = {
    'first_name': 'Test',
    'last_name': 'Student',
    'email': 'test.student@college.edu',
    'phone': '9876543210',
    'date_of_birth': '2000-01-15',
    'enrollment_date': '2024-08-01',
    'address': '123 Test Street, Hyderabad',
    'admission_category': 'EAMCET',
    'program': 'Computer Science and Engineering'
}

print("Testing student self-registration...")
print(f"Initial RegistrationRequests count: {RegistrationRequest.objects.count()}")

# Create form instance and validate
form = StudentSelfRegistrationForm(data=test_data)
if form.is_valid():
    print("Form is valid, saving student...")
    student = form.save()
    print(f"Student created: {student.full_name} (Reg: {student.registration_number})")
    
    # Create RegistrationRequest
    registration_request = RegistrationRequest.objects.create(
        student=student,
        status='PENDING'
    )
    print(f"RegistrationRequest created: ID {registration_request.id}, Status: {registration_request.status}")
else:
    print("Form validation errors:")
    for field, errors in form.errors.items():
        print(f"  {field}: {errors}")

print(f"Final RegistrationRequests count: {RegistrationRequest.objects.count()}")

# Show all requests
print("\nAll RegistrationRequests:")
for req in RegistrationRequest.objects.all():
    print(f"- {req.student.full_name}: {req.status} (ID: {req.id})")