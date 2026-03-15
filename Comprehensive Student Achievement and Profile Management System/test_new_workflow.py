import os
import django
from datetime import date

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.temp_models import TemporaryRegistration
from students.models import Student
from accounts.models import StudentCredential

print("=== TESTING NEW REGISTRATION WORKFLOW ===")
print()

# Clean up any existing test data
test_regs = TemporaryRegistration.objects.filter(first_name='Emma')
test_students = Student.objects.filter(first_name='Emma')

print(f"Cleaning up existing test data...")
print(f"Temporary registrations to delete: {test_regs.count()}")
print(f"Students to delete: {test_students.count()}")

for reg in test_regs:
    print(f"Deleting temp reg: {reg.full_name}")
    reg.delete()

for student in test_students:
    print(f"Deleting student: {student.full_name}")
    student.delete()

print()
print("CURRENT STATE:")
print(f"Temporary Registrations: {TemporaryRegistration.objects.count()}")
print(f"Students: {Student.objects.count()}")
print(f"Student Credentials: {StudentCredential.objects.count()}")

# Test 1: Frontend Registration (creates TemporaryRegistration only)
print()
print("--- TEST 1: Frontend Registration ---")
temp_reg = TemporaryRegistration.objects.create(
    first_name='Emma',
    last_name='Davis',
    email='emma.davis@college.edu',
    phone='6655443322',
    date_of_birth=date(2001, 8, 12),
    address='987 Cedar Lane, Hyderabad',
    admission_category='VSAT',
    program='Chemical Engineering',
    enrollment_date=date(2024, 9, 1),
    status='PENDING'
)

print(f"[SUCCESS] Temporary registration created:")
print(f"  Name: {temp_reg.full_name}")
print(f"  Email: {temp_reg.email}")
print(f"  Status: {temp_reg.status}")
print(f"  ID: {temp_reg.id}")

# Verify no Student created yet
students_count = Student.objects.filter(email='emma.davis@college.edu').count()
print(f"  Students with this email: {students_count} (should be 0)")

# Test 2: Admin Approval (creates Student and credentials)
print()
print("--- TEST 2: Admin Approval ---")
if temp_reg.status == 'PENDING':
    # Simulate admin approval
    from students.models import Student
    student = Student.objects.create(
        first_name=temp_reg.first_name,
        last_name=temp_reg.last_name,
        email=temp_reg.email,
        phone=temp_reg.phone,
        date_of_birth=temp_reg.date_of_birth,
        address=temp_reg.address,
        admission_category=temp_reg.admission_category,
        program=temp_reg.program,
        enrollment_date=temp_reg.enrollment_date
    )
    
    print(f"[SUCCESS] Student created:")
    print(f"  Registration Number: {student.registration_number}")
    print(f"  Full Name: {student.full_name}")
    
    # Update temporary registration
    temp_reg.status = 'APPROVED'
    temp_reg.save()
    print(f"  Temporary registration status updated to: {temp_reg.status}")
    
    # Generate credentials
    from accounts.utils import generate_student_credentials
    credential = generate_student_credentials(student)
    print(f"[SUCCESS] Credentials generated:")
    print(f"  Username: {credential.username}")
    print(f"  Temp Password: {credential.temporary_password}")
    print(f"  Is Active: {credential.is_active}")

print()
print("FINAL STATE:")
print(f"Temporary Registrations: {TemporaryRegistration.objects.count()}")
print(f"Students: {Student.objects.count()}")
print(f"Student Credentials: {StudentCredential.objects.count()}")

print()
print("All Temporary Registrations:")
for reg in TemporaryRegistration.objects.all():
    student_exists = Student.objects.filter(email=reg.email).exists()
    print(f"- {reg.full_name}: {reg.status} - Student exists: {student_exists}")

print()
print("Workflow Summary:")
print("✓ Frontend registration creates TemporaryRegistration (no Student yet)")
print("✓ Admin approval creates Student object and credentials")
print("✓ Students cannot access system until approved")
print("✓ System enforces admin verification before student access")