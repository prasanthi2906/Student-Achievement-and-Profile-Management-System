#!/usr/bin/env python
"""
Pre-presentation System Check Script
"""

import os
import django
import sys

def check_system():
    print("=" * 50)
    print("COMPREHENSIVE STUDENT MANAGEMENT SYSTEM")
    print("PRE-PRESENTATION SYSTEM CHECK")
    print("=" * 50)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
    
    try:
        django.setup()
        print("[SUCCESS] Django setup successful")
    except Exception as e:
        print(f"[ERROR] Django setup failed: {e}")
        return False
    
    # Check models
    try:
        from accounts.models import CustomUser, RegistrationRequest, StudentCredential
        from accounts.temp_models import TemporaryRegistration
        from students.models import Student
        from documents.models import Document
        from achievements.models import Achievement
        
        print("[SUCCESS] All models imported successfully")
    except Exception as e:
        print(f"[ERROR] Model import failed: {e}")
        return False
    
    # Check database counts
    print("\nDATABASE STATUS:")
    print(f"  Users: {CustomUser.objects.count()}")
    print(f"  Students: {Student.objects.count()}")
    print(f"  Documents: {Document.objects.count()}")
    print(f"  Achievements: {Achievement.objects.count()}")
    print(f"  Registration Requests: {RegistrationRequest.objects.count()}")
    print(f"  Temporary Registrations: {TemporaryRegistration.objects.count()}")
    print(f"  Student Credentials: {StudentCredential.objects.count()}")
    
    # Check admin functionality
    try:
        from accounts import admin as accounts_admin
        from students import admin as students_admin
        from documents import admin as documents_admin
        from achievements import admin as achievements_admin
        
        print("[SUCCESS] Admin modules loaded successfully")
    except Exception as e:
        print(f"[ERROR] Admin module loading failed: {e}")
        return False
    
    # Test format_html functionality
    try:
        from django.utils.html import format_html
        test1 = format_html('<span style="color: green;">{} Verified</span>', '&#10003;')
        test2 = format_html('<span class="badge {}">{}</span>', 'success', 'APPROVED')
        print("[SUCCESS] format_html functions working correctly")
    except Exception as e:
        print(f"[ERROR] format_html test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("ALL SYSTEM CHECKS PASSED!")
    print("Your presentation system is ready!")
    print("=" * 50)
    
    print("\nQUICK ACCESS:")
    print("  Homepage: http://127.0.0.1:8000")
    print("  Admin: http://127.0.0.1:8000/admin/")
    print("  Registration: http://127.0.0.1:8000/students/self-register/")
    
    return True

if __name__ == "__main__":
    success = check_system()
    if success:
        print("\nReady for your hackathon presentation!")
        sys.exit(0)
    else:
        print("\nPlease fix the issues before presenting!")
        sys.exit(1)