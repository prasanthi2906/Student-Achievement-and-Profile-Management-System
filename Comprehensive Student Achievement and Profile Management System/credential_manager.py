#!/usr/bin/env python
"""
Student Credential Management Tool
View existing credentials or generate new ones for students
"""

import os
import django
import sys

def manage_student_credentials():
    print("=" * 60)
    print("STUDENT CREDENTIAL MANAGEMENT")
    print("=" * 60)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
    django.setup()
    
    try:
        from students.models import Student
        from accounts.models import StudentCredential
        from accounts.utils import generate_student_credentials
        
        while True:
            print("\nOptions:")
            print("1. View all student credentials")
            print("2. Generate credentials for a specific student")
            print("3. Generate credentials for all students without credentials")
            print("4. Reset credentials for a student")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                # View all credentials
                credentials = StudentCredential.objects.select_related('student').all()
                print(f"\nFound {credentials.count()} student credentials:")
                print("-" * 80)
                print(f"{'Name':<20} {'Reg #':<12} {'Username':<15} {'Password':<12} {'Active'}")
                print("-" * 80)
                
                for cred in credentials:
                    active_status = "Yes" if cred.is_active else "No"
                    print(f"{cred.student.full_name:<20} {cred.student.registration_number:<12} {cred.username:<15} {cred.temporary_password:<12} {active_status}")
                
            elif choice == '2':
                # Generate for specific student
                reg_num = input("Enter student registration number: ").strip()
                try:
                    student = Student.objects.get(registration_number=reg_num)
                    credential = generate_student_credentials(student)
                    print(f"\n[SUCCESS] Credentials generated for {student.full_name}")
                    print(f"Username: {credential.username}")
                    print(f"Temporary Password: {credential.temporary_password}")
                    print(f"Registration Number: {student.registration_number}")
                except Student.DoesNotExist:
                    print("[ERROR] Student not found with that registration number")
                    
            elif choice == '3':
                # Generate for all students without credentials
                students_without_creds = Student.objects.filter(credential__isnull=True)
                if students_without_creds.exists():
                    print(f"\nFound {students_without_creds.count()} students without credentials")
                    confirm = input("Generate credentials for all? (y/N): ").strip().lower()
                    if confirm == 'y':
                        generated_count = 0
                        for student in students_without_creds:
                            generate_student_credentials(student)
                            generated_count += 1
                        print(f"[SUCCESS] Generated credentials for {generated_count} students")
                else:
                    print("[INFO] All students already have credentials")
                    
            elif choice == '4':
                # Reset credentials
                reg_num = input("Enter student registration number: ").strip()
                try:
                    student = Student.objects.get(registration_number=reg_num)
                    credential = generate_student_credentials(student)
                    print(f"\n[SUCCESS] Credentials reset for {student.full_name}")
                    print(f"New Username: {credential.username}")
                    print(f"New Temporary Password: {credential.temporary_password}")
                except Student.DoesNotExist:
                    print("[ERROR] Student not found with that registration number")
                    
            elif choice == '5':
                print("Goodbye!")
                break
                
            else:
                print("[ERROR] Invalid choice. Please enter 1-5.")
                
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manage_student_credentials()