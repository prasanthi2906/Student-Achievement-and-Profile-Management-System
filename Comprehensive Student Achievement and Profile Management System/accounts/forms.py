from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from students.models import Student

class StudentRegistrationForm(UserCreationForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        help_text="Select your student profile",
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'student', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Regular student user
        if commit:
            user.save()
        return user

class StudentLoginForm(forms.Form):
    registration_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)