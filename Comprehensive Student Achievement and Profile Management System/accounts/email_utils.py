from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_registration_confirmation(student):
    """Send confirmation email to student after registration"""
    subject = 'Student Registration Submitted'
    html_message = render_to_string('emails/registration_confirmation.html', {
        'student': student,
        'registration_number': student.registration_number
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [student.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_approval_notification(student):
    """Send approval notification to student"""
    subject = 'Student Registration Approved'
    html_message = render_to_string('emails/registration_approved.html', {
        'student': student,
        'registration_number': student.registration_number
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [student.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_admin_notification(student):
    """Notify admin about new registration"""
    subject = f'New Student Registration - {student.registration_number}'
    html_message = render_to_string('emails/admin_notification.html', {
        'student': student,
        'registration_number': student.registration_number
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=False,
    )