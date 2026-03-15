import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Student
from documents.models import Document
from achievements.models import Achievement

print("=== Django Models Test ===")

# Test Student model
print(f"Total Students: {Student.objects.count()}")

# Test Document model
print(f"Total Documents: {Document.objects.count()}")

# Test Achievement model
print(f"Total Achievements: {Achievement.objects.count()}")

print("All models are working correctly!")