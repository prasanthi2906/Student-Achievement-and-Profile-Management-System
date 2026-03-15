from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentUploadForm
from students.models import Student

@login_required
def document_list(request):
    """List all documents"""
    documents = Document.objects.select_related('student').all().order_by('-uploaded_at')
    return render(request, 'documents/list.html', {'documents': documents})

@login_required
def upload_document(request):
    """Upload new document"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def document_detail(request, pk):
    """View document details"""
    document = get_object_or_404(Document.objects.select_related('student'), pk=pk)
    return render(request, 'documents/detail.html', {'document': document})

@login_required
def document_verify(request, pk):
    """Verify a document"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.verified = True
        document.verified_by = request.user
        document.save()
        messages.success(request, 'Document verified successfully!')
        return redirect('document_detail', pk=document.pk)
    
    return render(request, 'documents/verify.html', {'document': document})

@login_required
def document_delete(request, pk):
    """Delete document"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('document_list')
    
    return render(request, 'documents/delete.html', {'document': document})
