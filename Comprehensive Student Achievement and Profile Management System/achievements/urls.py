from django.urls import path
from . import views

urlpatterns = [
    path('achievements/', views.achievement_list, name='achievement_list'),
    path('achievements/add/', views.add_achievement, name='add_achievement'),
    path('achievements/<int:pk>/', views.achievement_detail, name='achievement_detail'),
    path('achievements/<int:pk>/approve/', views.achievement_approve, name='achievement_approve'),
    path('achievements/<int:pk>/reject/', views.achievement_reject, name='achievement_reject'),
    path('achievements/<int:pk>/delete/', views.achievement_delete, name='achievement_delete'),
]