from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('history/', views.history, name='history'),
    path('update/<int:pk>/', views.update_transaction, name='update_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('clear_budget/', views.clear_budget, name='clear_budget'),  # Add this line
]
