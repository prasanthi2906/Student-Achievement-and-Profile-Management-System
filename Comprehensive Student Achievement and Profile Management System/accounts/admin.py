from django.contrib import admin
from django.utils import timezone
from .models import StudentCredential
from .temp_models import TemporaryRegistration
from students.models import Student
from accounts.utils import generate_student_credentials, send_approval_notification_email

@admin.register(StudentCredential)
class StudentCredentialAdmin(admin.ModelAdmin):
    list_display = ['username', 'student', 'temporary_password', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'student__first_name', 'student__last_name', 'student__registration_number']
    readonly_fields = ['created_at', 'activated_at']

@admin.register(TemporaryRegistration)
class TemporaryRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'admission_category']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['submitted_at', 'reviewed_at']
    actions = ['approve_registrations', 'reject_registrations']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address')
        }),
        ('Academic Information', {
            'fields': ('admission_category', 'program', 'enrollment_date')
        }),
        ('Request Status', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Review Information', {
            'fields': ('reviewed_at', 'reviewed_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )
    
    def approve_registrations(self, request, queryset):
        """Approve selected temporary registrations and create actual students"""
        approved_count = 0
        email_sent_count = 0
        already_registered_count = 0
        duplicate_in_batch_count = 0
        
        # Track emails processed in this batch to detect duplicates within the same approval action
        processed_emails = set()
        
        for temp_reg in queryset:
            if temp_reg.status == 'PENDING':
                # Check for duplicate within this batch
                if temp_reg.email in processed_emails:
                    temp_reg.status = 'REJECTED'
                    temp_reg.rejection_reason = f"Duplicate within batch: another registration with {temp_reg.email} was already approved in this action"
                    temp_reg.reviewed_at = timezone.now()
                    temp_reg.reviewed_by = request.user
                    temp_reg.save()
                    duplicate_in_batch_count += 1
                    continue
                
                # Check if student with this email already exists
                existing_student = Student.objects.filter(email=temp_reg.email).first()
                if existing_student:
                    # Student was already registered (e.g. via direct registration).
                    # Mark as approved since the student record already exists.
                    temp_reg.status = 'APPROVED'
                    temp_reg.reviewed_at = timezone.now()
                    temp_reg.reviewed_by = request.user
                    temp_reg.rejection_reason = None
                    temp_reg.save()
                    
                    # Generate credentials if they don't exist yet
                    if not StudentCredential.objects.filter(student=existing_student).exists():
                        generate_student_credentials(existing_student)
                    
                    already_registered_count += 1
                    processed_emails.add(temp_reg.email)
                    continue
                
                # Create actual Student object
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
                
                # Send approval notification email
                if send_approval_notification_email(temp_reg):
                    email_sent_count += 1
                
                # Update temporary registration
                temp_reg.status = 'APPROVED'
                temp_reg.reviewed_at = timezone.now()
                temp_reg.reviewed_by = request.user
                temp_reg.save()
                
                # Create credentials (this will also send credential email)
                generate_student_credentials(student)
                
                approved_count += 1
                processed_emails.add(temp_reg.email)
        
        # Provide feedback to admin
        if approved_count > 0:
            self.message_user(
                request, 
                f'{approved_count} temporary registrations were approved and students created. '
                f'{email_sent_count} approval notifications sent successfully.'
            )
        
        if already_registered_count > 0:
            self.message_user(
                request,
                f'{already_registered_count} registrations were auto-approved (students were already registered directly).',
                level='info'
            )
        
        if duplicate_in_batch_count > 0:
            self.message_user(
                request,
                f'{duplicate_in_batch_count} registrations were rejected due to duplicate emails within the same batch.',
                level='warning'
            )
    approve_registrations.short_description = "Approve selected registrations"
    
    def reject_registrations(self, request, queryset):
        """Reject selected temporary registrations"""
        rejected_count = 0
        for temp_reg in queryset:
            if temp_reg.status == 'PENDING':
                temp_reg.status = 'REJECTED'
                temp_reg.reviewed_at = timezone.now()
                temp_reg.reviewed_by = request.user
                temp_reg.save()
                rejected_count += 1
        
        self.message_user(request, f'{rejected_count} temporary registrations were rejected.')
    reject_registrations.short_description = "Reject selected registrations"