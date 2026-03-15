from django.db import models
from django.conf import settings
from datetime import date

class Student(models.Model):
    # Updated registration number format
    BATCH_PREFIX = "231"  # You can change this based on year
    DEPARTMENT_CODE = "FA"  # Department code
    SEQUENCE_START = 4001  # Starting sequence number
    
    # Auto-generated registration number
    registration_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    # Admission Information
    ADMISSION_CATEGORIES = [
        ('VSAT', 'VSAT'),
        ('EAMCET', 'EAMCET'),
        ('JEE', 'JEE Main/Advanced'),
        ('MANAGEMENT', 'Management Quota'),
        ('OTHER', 'Other'),
    ]
    admission_category = models.CharField(max_length=20, choices=ADMISSION_CATEGORIES)
    program = models.CharField(max_length=100)
    enrollment_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def save(self, *args, **kwargs):
        # Generate registration number if not exists
        if not self.registration_number:
            # Get the last student to determine next sequence
            last_student = Student.objects.order_by('-id').first()
            if last_student and last_student.registration_number.startswith(f"{self.BATCH_PREFIX}{self.DEPARTMENT_CODE}"):
                # Extract the numeric part and increment
                try:
                    last_sequence = int(last_student.registration_number[6:])
                    next_sequence = last_sequence + 1
                except ValueError:
                    next_sequence = self.SEQUENCE_START
            else:
                next_sequence = self.SEQUENCE_START
            
            self.registration_number = f"{self.BATCH_PREFIX}{self.DEPARTMENT_CODE}{next_sequence:05d}"
        super().save(*args, **kwargs)
