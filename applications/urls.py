from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
