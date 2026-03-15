from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/verify/', views.document_verify, name='document_verify'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
]