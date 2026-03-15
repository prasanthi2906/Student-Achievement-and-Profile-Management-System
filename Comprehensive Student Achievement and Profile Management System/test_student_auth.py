import os
import django
from django.test import TestCase, Client
from django.urls import reverse
from students.models import Student
from accounts.models import StudentCredential

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

class StudentAuthTestCase(TestCase):
    def setUp(self):
        # Create a test student with credentials
        self.student = Student.objects.create(
            registration_number='TEST001',
            first_name='Test',
            last_name='Student',
            email='test@student.com'
        )
        
        # Create credentials for the student
        self.credential = StudentCredential.objects.create(
            student=self.student,
            username='test001',
            temporary_password='testpass123',
            is_active=False
        )
        
        self.client = Client()

    def test_student_login_success(self):
        """Test successful student login"""
        response = self.client.post(reverse('student_login'), {
            'registration_number': 'TEST001',
            'password': 'testpass123'
        })
        
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('student_dashboard'))
        
        # Check session variables
        session = self.client.session
        self.assertTrue(session.get('is_student'))
        self.assertEqual(session.get('student_id'), self.student.id)
        
        # Check that account was activated
        self.credential.refresh_from_db()
        self.assertTrue(self.credential.is_active)

    def test_student_document_upload_access(self):
        """Test that logged-in student can access document upload"""
        # First login
        self.client.post(reverse('student_login'), {
            'registration_number': 'TEST001',
            'password': 'testpass123'
        })
        
        # Try to access document upload
        response = self.client.get(reverse('student_document_upload'))
        
        # Should be accessible (status 200) not redirect to admin login
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload Document')

    def test_unauthorized_access_redirects(self):
        """Test that unauthorized users are redirected to student login"""
        response = self.client.get(reverse('student_document_upload'))
        
        # Should redirect to student login
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('student_login'), response.url)

if __name__ == '__main__':
    import unittest
    unittest.main()