from django.contrib import admin
from django.utils import timezone
from .temp_models import TemporaryRegistration
from students.models import Student
from accounts.utils import generate_student_credentials

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
        for temp_reg in queryset:
            if temp_reg.status == 'PENDING':
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
                
                # Update temporary registration
                temp_reg.status = 'APPROVED'
                temp_reg.reviewed_at = timezone.now()
                temp_reg.reviewed_by = request.user
                temp_reg.save()
                
                # Create credentials
                generate_student_credentials(student)
                
                approved_count += 1
        
        self.message_user(request, f'{approved_count} temporary registrations were approved and students created.')
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