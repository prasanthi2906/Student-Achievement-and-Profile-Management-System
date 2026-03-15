import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import StudentCredential, RegistrationRequest

def generate_temporary_password(length=8):
    """Generate a temporary password"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_student_credentials(student):
    """Generate username and temporary password for student"""
    # Generate username (registration number)
    username = student.registration_number.lower()
    
    # Generate temporary password
    temp_password = generate_temporary_password()
    
    # Create or update credential record
    credential, created = StudentCredential.objects.get_or_create(
        student=student,
        defaults={
            'username': username,
            'temporary_password': temp_password,
            'is_active': False
        }
    )
    
    if not created:
        credential.temporary_password = temp_password
        credential.is_active = False
        credential.save()
    
    # Send email with credentials
    send_credential_email(student, username, temp_password)
    
    return credential

def activate_student_account(student):
    """Activate student account after they use temporary credentials"""
    try:
        credential = StudentCredential.objects.get(student=student)
        credential.is_active = True
        credential.activated_at = timezone.now()
        credential.save()
        return True
    except StudentCredential.DoesNotExist:
        return False

def send_credential_email(student, username, password):
    """Send credentials to student via email"""
    try:
        # Create email subject
        subject = f"Student Portal Credentials - {student.full_name}"
        
        # Create email context
        context = {
            'student': student,
            'username': username,
            'password': password,
            'login_url': 'http://127.0.0.1:8000/student/login/',
            'portal_name': 'Student Achievement and Profile Management System'
        }
        
        # Render HTML email template
        html_content = render_to_string('emails/credential_email.html', context)
        text_content = strip_tags(html_content)
        
        # Create email message
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [student.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        
        print(f"[OK] Credentials email sent successfully to {student.email}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send email to {student.email}: {str(e)}")
        # Fallback to console output
        print(f"CREDENTIALS FOR {student.full_name}:")
        print(f"Username: {username}")
        print(f"Temporary Password: {password}")
        print(f"Registration Number: {student.registration_number}")
        print("---")
        return False

def send_approval_notification_email(temp_registration):
    """Send notification to student when their registration is approved"""
    try:
        subject = f"Registration Approved - Welcome to Student Portal"
        
        context = {
            'student_name': temp_registration.full_name,
            'approval_date': timezone.now().strftime("%B %d, %Y"),
            'login_instructions': 'You will receive your login credentials in a separate email shortly.',
            'contact_email': settings.DEFAULT_FROM_EMAIL,
            'portal_name': 'Student Achievement and Profile Management System'
        }
        
        html_content = render_to_string('emails/approval_notification.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [temp_registration.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        email.send()
        print(f"[OK] Approval notification sent to {temp_registration.email}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send approval notification: {str(e)}")
        return False