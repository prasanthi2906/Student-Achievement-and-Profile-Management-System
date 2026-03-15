import os
from django import forms
from .models import Document
from students.models import Student

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['student', 'document_type', 'title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order students by registration number
        self.fields['student'].queryset = Student.objects.all().order_by('registration_number')
        self.fields['student'].widget.attrs.update({'class': 'form-select'})
        self.fields['document_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"File extension '{ext}' is not allowed. Allowed extensions: {', '.join(allowed_extensions)}")
        
        return file