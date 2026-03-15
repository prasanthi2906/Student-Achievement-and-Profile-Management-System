import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from accounts.models import RegistrationRequest

print(f"Total RegistrationRequests: {RegistrationRequest.objects.count()}")
print("Existing requests:")
for req in RegistrationRequest.objects.all():
    print(f"- {req.student.full_name}: {req.status} (ID: {req.id})")