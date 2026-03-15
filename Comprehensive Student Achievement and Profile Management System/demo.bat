@echo off
echo 🚀 Starting Student Management System Demo...
echo ==============================================

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if Django is installed
echo Checking Django installation...
python -c "import django; print(f'Django version: {django.get_version()}')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Django not found. Installing...
    pip install django
)

REM Run migrations if needed
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser if doesn't exist
echo Setting up admin user...
python create_superuser.py

REM Create sample data
echo Creating sample student data...
python create_test_student.py

REM Start the server
echo Starting development server...
echo 📱 Access the application at: http://127.0.0.1:8000/
echo 🔒 Admin panel at: http://127.0.0.1:8000/admin/
echo    Username: admin
echo    Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ==============================================

python manage.py runserver
pause