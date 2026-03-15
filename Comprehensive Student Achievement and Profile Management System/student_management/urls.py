"""
URL configuration for student_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from students import views as student_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', student_views.home, name='home'),
    path('', include('students.urls')),
    path('', include('documents.urls')),
    path('', include('achievements.urls')),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', account_views.custom_logout, name='logout'),
    # Student Authentication
    path('student/login/', account_views.student_login, name='student_login'),
    path('student/dashboard/', account_views.student_dashboard, name='student_dashboard'),
    path('student/logout/', account_views.student_logout, name='student_logout'),
    # Student Self-Service URLs
    path('student/upload-document/', account_views.student_document_upload, name='student_document_upload'),
    path('student/submit-achievement/', account_views.student_achievement_submit, name='student_achievement_submit'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)