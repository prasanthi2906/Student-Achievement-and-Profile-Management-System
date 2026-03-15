from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Achievement
from .forms import AchievementForm
from students.models import Student

@login_required
def achievement_list(request):
    """List all achievements"""
    achievements = Achievement.objects.select_related('student').all().order_by('-date', '-created_at')
    return render(request, 'achievements/list.html', {'achievements': achievements})

@login_required
def add_achievement(request):
    """Add new achievement"""
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save()
            messages.success(request, 'Achievement added successfully!')
            return redirect('achievement_detail', pk=achievement.pk)
    else:
        form = AchievementForm()
    
    return render(request, 'achievements/add.html', {'form': form})

@login_required
def achievement_detail(request, pk):
    """View achievement details"""
    achievement = get_object_or_404(Achievement.objects.select_related('student'), pk=pk)
    return render(request, 'achievements/detail.html', {'achievement': achievement})

@login_required
def achievement_approve(request, pk):
    """Approve an achievement"""
    achievement = get_object_or_404(Achievement, pk=pk)
    
    if request.method == 'POST':
        achievement.status = 'APPROVED'
        achievement.verified_by = request.user
        achievement.save()
        messages.success(request, 'Achievement approved successfully!')
        return redirect('achievement_detail', pk=achievement.pk)
    
    return render(request, 'achievements/approve.html', {'achievement': achievement})

@login_required
def achievement_reject(request, pk):
    """Reject an achievement"""
    achievement = get_object_or_404(Achievement, pk=pk)
    
    if request.method == 'POST':
        achievement.status = 'REJECTED'
        achievement.rejection_reason = request.POST.get('rejection_reason', '')
        achievement.save()
        messages.success(request, 'Achievement rejected successfully!')
        return redirect('achievement_detail', pk=achievement.pk)
    
    return render(request, 'achievements/reject.html', {'achievement': achievement})

@login_required
def achievement_delete(request, pk):
    """Delete achievement"""
    achievement = get_object_or_404(Achievement, pk=pk)
    
    if request.method == 'POST':
        achievement.delete()
        messages.success(request, 'Achievement deleted successfully!')
        return redirect('achievement_list')
    
    return render(request, 'achievements/delete.html', {'achievement': achievement})
