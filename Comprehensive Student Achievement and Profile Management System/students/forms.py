from django import forms
from .models import Student
from documents.models import Document
from achievements.models import Achievement
from accounts.temp_models import TemporaryRegistration
import os

class StudentSelfRegistrationForm(forms.ModelForm):
    # Document fields
    document_type = forms.ChoiceField(
        choices=[('', '--- Select Document Type ---')] + Document.DOCUMENT_TYPES,
        required=False,
        label="Document Type"
    )
    document_title = forms.CharField(
        max_length=200, 
        required=False,
        label="Document Title"
    )
    document_file = forms.FileField(
        required=False,
        label="Upload Document",
        help_text="Supported formats: PDF, JPG, JPEG, PNG, DOC, DOCX (Max 5MB)"
    )
    
    # Achievement fields
    achievement_title = forms.CharField(
        max_length=200, 
        required=False,
        label="Achievement Title"
    )
    achievement_category = forms.ChoiceField(
        choices=[('', '--- Select Category ---')] + Achievement.ACHIEVEMENT_CATEGORIES,
        required=False,
        label="Achievement Category"
    )
    achievement_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description of your achievement...'}),
        required=False,
        label="Description"
    )
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'address', 'admission_category', 
            'program', 'enrollment_date'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'program': forms.TextInput(attrs={'placeholder': 'Enter program/course name'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Skip duplicate check when editing an existing student
        if self.instance and self.instance.pk:
            if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A student with this email already exists.")
        else:
            if Student.objects.filter(email=email).exists():
                raise forms.ValidationError("A student with this email already exists.")
            if TemporaryRegistration.objects.filter(email=email, status='PENDING').exists():
                raise forms.ValidationError("A registration with this email is already pending approval.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (len(phone) < 10 or len(phone) > 15):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
    
    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')
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
    
    def save(self, commit=True):
        student = super().save(commit=False)
        
        if commit:
            student.save()
            
            # Save document if provided
            if (self.cleaned_data.get('document_type') and 
                self.cleaned_data.get('document_title') and 
                self.cleaned_data.get('document_file')):
                
                Document.objects.create(
                    student=student,
                    document_type=self.cleaned_data['document_type'],
                    title=self.cleaned_data['document_title'],
                    file=self.cleaned_data['document_file']
                )
            
            # Save achievement if provided
            if (self.cleaned_data.get('achievement_title') and 
                self.cleaned_data.get('achievement_category') and 
                self.cleaned_data.get('achievement_description')):
                
                Achievement.objects.create(
                    student=student,
                    title=self.cleaned_data['achievement_title'],
                    category=self.cleaned_data['achievement_category'],
                    description=self.cleaned_data['achievement_description'],
                    date=student.enrollment_date  # Use enrollment date as achievement date
                )
        
        return student

class StudentDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class StudentAchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'title', 'category', 'description', 
            'date', 'organizing_body', 'certificate', 'proof_document'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'organizing_body': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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