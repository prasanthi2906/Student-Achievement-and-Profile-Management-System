import os
import django
from django.core.mail import EmailMessage
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

def test_email_settings():
    """Test your email configuration"""
    
    print("=== EMAIL CONFIGURATION CHECK ===")
    print(f"Gmail Address: {settings.EMAIL_HOST_USER}")
    print(f"App Password Length: {len(settings.EMAIL_HOST_PASSWORD.replace(' ', ''))} characters")
    print()
    
    # Test email - replace with your actual email to test
    test_recipient = input("Enter your email address to receive test email: ").strip()
    
    if not test_recipient:
        print("No email entered. Test cancelled.")
        return
    
    try:
        email = EmailMessage(
            subject='Student Portal - Test Email',
            body='Success! Your Gmail SMTP configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[test_recipient]
        )
        
        print("Sending test email...")
        email.send()
        print("✅ Test email sent successfully!")
        print("Check your inbox (and spam folder) for the test message.")
        
    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify App Password is correct (16 characters)")
        print("2. Check Gmail 2FA is enabled")
        print("3. Ensure no typos in email address")
        print("4. Check internet connection")

if __name__ == "__main__":
    test_email_settings()