from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff Member'),
        ('ADMIN', 'Administrator'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='STUDENT')
    student_profile = models.OneToOneField('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='user_account')
    
    # Override groups and user_permissions with custom related_names
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_student(self):
        return self.user_type == 'STUDENT'
    
    @property
    def is_staff_member(self):
        return self.user_type == 'STAFF'
    
    @property
    def is_administrator(self):
        return self.user_type == 'ADMIN'

# RegistrationRequest model has been deprecated in favor of TemporaryRegistration
# Keeping empty model to avoid migration issues, but not used in application
class RegistrationRequest(models.Model):
    # Empty model to maintain database compatibility
    # All new registrations should use TemporaryRegistration model
    pass
    
    class Meta:
        managed = False  # Don't manage this table

class StudentCredential(models.Model):
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='credential')
    username = models.CharField(max_length=50, unique=True)
    temporary_password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.student.full_name}"
    
    class Meta:
        verbose_name = "Student Credential"
        verbose_name_plural = "Student Credentials"