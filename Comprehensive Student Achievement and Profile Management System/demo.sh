#!/bin/bash
# Student Management System Demo Script

echo "🚀 Starting Student Management System Demo..."
echo "=============================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || venv\Scripts\activate.bat
fi

# Check if Django is installed
echo "Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')" || {
    echo "❌ Django not found. Installing..."
    pip install django
}

# Run migrations if needed
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if doesn't exist
echo "Setting up admin user..."
python create_superuser.py

# Create sample data
echo "Creating sample student data..."
python create_test_student.py

# Start the server
echo "Starting development server..."
echo "📱 Access the application at: http://127.0.0.1:8000/"
echo "🔒 Admin panel at: http://127.0.0.1:8000/admin/"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="

python manage.py runserver