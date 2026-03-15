from django.contrib import admin
from django.utils.html import format_html
from .models import Achievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'category', 'date', 'status_badge']
    list_filter = ['category', 'status', 'date']
    search_fields = ['student__first_name', 'student__last_name', 'student__registration_number', 'title']
    readonly_fields = ['created_at', 'updated_at', 'verified_at']
    actions = ['approve_achievements', 'reject_achievements']
    
    fieldsets = (
        ('Achievement Information', {
            'fields': ('student', 'title', 'category', 'description', 'date', 'organizing_body')
        }),
        ('Supporting Documents', {
            'fields': ('certificate', 'proof_document'),
            'classes': ('collapse',)
        }),
        ('Verification Status', {
            'fields': ('status', 'verified_by', 'verified_at', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        badge_class = obj.status_badge_class()
        return format_html('<span class="badge {}">{}</span>', badge_class, obj.status)
    status_badge.short_description = 'Status'
    
    def approve_achievements(self, request, queryset):
        updated = queryset.update(status='APPROVED', verified_by=request.user)
        self.message_user(request, f'{updated} achievements were successfully approved.')
    approve_achievements.short_description = "Approve selected achievements"
    
    def reject_achievements(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated} achievements were rejected.')
    reject_achievements.short_description = "Reject selected achievements"
