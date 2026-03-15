from django.db import models
from django.conf import settings
from students.models import Student

class Achievement(models.Model):
    ACHIEVEMENT_CATEGORIES = [
        ('HACKATHON', 'Hackathon'),
        ('INTERNSHIP', 'Internship'),
        ('RESEARCH', 'Research Publication'),
        ('TECH_COMP', 'Technical Competition'),
        ('SPORTS', 'Sports Achievement'),
        ('CULTURAL', 'Cultural Activity'),
        ('WORKSHOP', 'Workshop/Seminar'),
        ('OTHER', 'Other Achievement'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=ACHIEVEMENT_CATEGORIES)
    description = models.TextField()
    date = models.DateField()
    organizing_body = models.CharField(max_length=200)
    
    # Supporting documents
    certificate = models.FileField(upload_to='achievements/certificates/', null=True, blank=True)
    proof_document = models.FileField(upload_to='achievements/proofs/', null=True, blank=True)
    
    # Verification status
    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_achievements'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
    
    def __str__(self):
        return f"{self.student.registration_number} - {self.title} ({self.category})"
    
    def status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'PENDING': 'bg-warning',
            'APPROVED': 'bg-success',
            'REJECTED': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')
