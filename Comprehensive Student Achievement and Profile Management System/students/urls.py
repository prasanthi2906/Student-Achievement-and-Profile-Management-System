from django.urls import path
from . import views
from accounts import views as account_views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/register/', views.register_student, name='register_student'),
    path('students/self-register/', views.student_self_register, name='student_self_register'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Student self-service URLs
    path('student/dashboard/', account_views.student_dashboard, name='student_dashboard'),
    path('student/upload-document/', account_views.student_document_upload, name='student_document_upload'),
    path('student/submit-achievement/', account_views.student_achievement_submit, name='student_achievement_submit'),
]