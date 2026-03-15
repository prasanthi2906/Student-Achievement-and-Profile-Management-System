from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'email', 'program', 'admission_category', 'age']
    list_filter = ['program', 'admission_category', 'enrollment_date']
    search_fields = ['registration_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['registration_number', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    # Enable deletion actions
    actions = ['delete_selected']
    
    fieldsets = (
        ('Registration Information', {
            'fields': ('registration_number',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address')
        }),
        ('Academic Information', {
            'fields': ('admission_category', 'program', 'enrollment_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of students"""
        return True
    
    def delete_queryset(self, request, queryset):
        """Handle bulk deletion of students"""
        # This will cascade delete related documents and achievements
        for obj in queryset:
            obj.delete()
