
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.student_list, name='student_list'),

    path('add/', views.student_add, name='student_add'),

    path('edit/<int:pk>/', views.student_edit, name='student_edit'),

    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:id>/', views.student_detail, name='student_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
