from django.db import models
from django.conf import settings
from students.models import Student

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('MARKSHEET', 'Marksheet/Memo'),
        ('AADHAAR', 'Aadhaar Card'),
        ('PAN', 'PAN Card'),
        ('VOTER_ID', 'Voter ID'),
        ('APAAR', 'APAAR ID'),
        ('ABC_ID', 'ABC ID'),
        ('OTHER', 'Other Documents'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def __str__(self):
        return f"{self.student.registration_number} - {self.document_type}: {self.title}"
    
    def verification_status(self):
        if self.verified:
            return "Verified"
        return "Pending Verification"
