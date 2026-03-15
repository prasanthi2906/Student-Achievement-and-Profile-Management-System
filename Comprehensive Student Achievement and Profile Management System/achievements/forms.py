import os
from django import forms
from .models import Achievement
from students.models import Student

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'student', 'title', 'category', 'description', 
            'date', 'organizing_body', 'certificate', 'proof_document'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'organizing_body': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order students by registration number
        self.fields['student'].queryset = Student.objects.all().order_by('registration_number')
        self.fields['student'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['certificate'].widget.attrs.update({'class': 'form-control'})
        self.fields['proof_document'].widget.attrs.update({'class': 'form-control'})
    
    def clean_certificate(self):
        certificate = self.cleaned_data.get('certificate')
        if certificate:
            self._validate_file(certificate, 'Certificate')
        return certificate
    
    def clean_proof_document(self):
        proof_document = self.cleaned_data.get('proof_document')
        if proof_document:
            self._validate_file(proof_document, 'Proof document')
        return proof_document
    
    def _validate_file(self, file, file_type):
        # Check file size (10MB limit for certificates/proofs)
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(f"{file_type} size must be under 10MB.")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_extensions:
            raise forms.ValidationError(f"{file_type} extension '{ext}' is not allowed. Allowed extensions: {', '.join(allowed_extensions)}")