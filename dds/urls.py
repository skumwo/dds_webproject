from django.urls import path
from . import views

urlpatterns = [
    path('', views.cashflow_list, name='cashflow_list'),
    path('create/', views.cashflow_create, name='cashflow_create'),
    path('edit/<int:pk>/', views.cashflow_edit, name='cashflow_edit'),
    path('delete/<int:pk>/', views.cashflow_delete, name='cashflow_delete'),

    path('dicts/', views.dicts_unified, name='dicts_unified'),

    path('ajax/get_categories/', views.get_categories, name='get_categories'),
    path('ajax/get_subcategories/', views.get_subcategories, name='get_subcategories'),
]

