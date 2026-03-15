import os
import django
from datetime import date

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Student

# Create a test student
student = Student.objects.create(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    phone="1234567890",
    date_of_birth=date(2000, 1, 15),
    address="123 Main Street, City, State",
    admission_category="JEE",
    program="Computer Science Engineering",
    enrollment_date=date(2024, 8, 1)
)

print(f"Created student: {student}")
print(f"Registration Number: {student.registration_number}")
print(f"Full Name: {student.full_name}")
print(f"Age: {student.age}")

# Test querying
all_students = Student.objects.all()
print(f"\nTotal students in database: {all_students.count()}")

for s in all_students:
    print(f"- {s.registration_number}: {s.full_name} ({s.program})")