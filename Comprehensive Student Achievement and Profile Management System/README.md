# Comprehensive Student Achievement and Profile Management System

A Django-based web application for managing student profiles, official documents, and achievements in educational institutions.

## Features

### Student Profile Management
- Complete student registration with auto-generated registration numbers
- Personal information management (name, contact details, address)
- Academic information (admission category, program, enrollment date)
- Age calculation and profile viewing

### Document Repository
- Secure storage of official documents:
  - Mark memos
  - Aadhaar card
  - PAN card
  - Voter ID
  - APAAR/ABC ID
  - Other verification documents
- File upload with validation (size and type checking)
- Document verification workflow
- Search and categorization

### Achievement Tracking
- Record various student achievements:
  - Hackathons
  - Internships
  - Research publications
  - Technical competitions
  - Sports achievements
  - Cultural activities
  - Workshops and seminars
- Certificate and proof document storage
- Approval/rejection workflow
- Achievement categorization

### Administrative Features
- Professional Django Admin interface
- Student search by registration number
- Document verification system
- Achievement approval workflow
- Statistics and reporting dashboard
- Role-based access control

## Technology Stack

- **Framework**: Django 6.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **File Storage**: Django Media Files
- **Authentication**: Django Auth System

## Installation

1. **Clone the repository** (if using version control):
   ```bash
   git clone <repository-url>
   cd student-management-system
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   Or use the provided script:
   ```bash
   python create_superuser.py
   ```
   Default credentials: username: `admin`, password: `admin123`

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Students/Administrators
1. **Register new students** through the registration form
2. **Upload documents** for verification
3. **Record achievements** with supporting certificates
4. **View student profiles** and their complete history

### For Administrators
1. **Login to admin panel** using superuser credentials
2. **Manage students, documents, and achievements**
3. **Verify documents** and approve achievements
4. **Generate reports** and statistics
5. **Search students** by registration number

## Project Structure

```
student_management/
├── student_management/     # Main project settings
├── students/              # Student management app
├── documents/             # Document storage app
├── achievements/          # Achievement tracking app
├── templates/             # HTML templates
├── static/               # CSS, JavaScript, images
├── media/                # Uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Key Components

### Models
- **Student**: Core student information with auto-generated registration numbers
- **Document**: Secure document storage with verification tracking
- **Achievement**: Achievement tracking with approval workflow

### Views
- Student registration and management
- Document upload and verification
- Achievement recording and approval
- Admin dashboard and reporting

### Admin Interface
- Customized admin panels for each model
- Search and filter capabilities
- Bulk actions for verification/approval
- Professional interface design

## Security Features

- CSRF protection
- SQL injection prevention
- File upload validation
- User authentication and authorization
- Secure password handling

## Development Commands

```bash
# Run development server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files (for production)
python manage.py collectstatic
```

## Testing

The system includes test data creation scripts:
- `create_test_student.py`: Creates sample student data
- `test_models.py`: Verifies model functionality

## Deployment

For production deployment:
1. Switch to PostgreSQL database
2. Configure environment variables
3. Set DEBUG=False
4. Configure ALLOWED_HOSTS
5. Use a production web server (Gunicorn/Nginx)
6. Set up SSL certificates

## Competition Advantages

This Django implementation provides:
- Professional admin interface impressing judges
- Built-in security features
- Scalable architecture
- Comprehensive feature set
- Clean, maintainable code
- Rapid development capabilities
- Industry-standard practices

## Support

For issues or questions:
1. Check the Django admin interface first
2. Review error messages in development console
3. Verify all migrations are applied
4. Ensure virtual environment is activated

## License

This project is developed for educational purposes and competition use.