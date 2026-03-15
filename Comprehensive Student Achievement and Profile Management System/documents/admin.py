from django.contrib import admin
from django.utils.html import format_html
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'title', 'uploaded_at', 'verification_status']
    list_filter = ['document_type', 'verified', 'uploaded_at']
    search_fields = ['student__first_name', 'student__last_name', 'student__registration_number', 'title']
    readonly_fields = ['uploaded_at', 'verified_at']
    actions = ['verify_documents', 'reject_documents']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('student', 'document_type', 'title', 'file')
        }),
        ('Verification Status', {
            'fields': ('verified', 'verified_by', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def verification_status(self, obj):
        if obj.verified:
            return format_html('<span style="color: green;">{} Verified</span>', '&#10003;')
        return format_html('<span style="color: orange;">{} Pending</span>', '&#9203;')
    verification_status.short_description = 'Status'
    
    def verify_documents(self, request, queryset):
        updated = queryset.update(verified=True, verified_by=request.user)
        self.message_user(request, f'{updated} documents were successfully verified.')
    verify_documents.short_description = "Mark selected documents as verified"
    
    def reject_documents(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f'{updated} documents were marked as not verified.')
    reject_documents.short_description = "Mark selected documents as not verified"
