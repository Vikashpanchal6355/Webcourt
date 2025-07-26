"""webcourt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.urls import path,include
from staff import views

urlpatterns=[
    path('login',views.login, name='login'),
    path('login_check/', views.login_check, name='login_check'),
    path('logout_user',views.logout_user,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    
    path('hearing/',views.hearing,name='hearing'),
    path('all_hearing/',views.all_hearing,name='all_hearing'),
    path('delete_hearing/<int:pk>/', views.delete_hearing, name='delete_hearing'),
    path('store_hearing',views.store_hearing,name='store_hearing'),
    path('edit_hearing/<int:id>/', views.edit_hearing, name='edit_hearing'),
    path('update_hearing/<int:id>', views.update_hearing, name='update_hearing'),

    path('all_cases/',views.all_cases,name='all_cases'),
    path('case_delete/<int:pk>/', views.case_delete, name='case_delete'),
    path('edit_case/<int:id>/', views.edit_case, name='edit_case'),
    path('update_case/<int:id>', views.update_case, name='update_case'),
    path('view_cases/<int:id>/', views.view_cases, name='view_cases'),

  
    path('add_evidence/', views.add_evidence, name='add_evidence'),
    path('store_evidence/', views.store_evidence, name='store_evidence'),
    path('details_evidence/<int:id>', views.details_evidence, name='details_evidence'),
    path('all_evidence/', views.all_evidence, name='all_evidence'),
    # path('delete_evidence/<int:id>', views.delete_evidence, name='delete_evidence'),
    # path('edit_evidence/<int:id>', views.edit_evidence, name='edit_evidence'),
    # path('update_evidence/<int:id>', views.update_evidence, name='update_evidence'),
]