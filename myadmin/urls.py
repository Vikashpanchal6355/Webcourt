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

from django.urls import path
from myadmin import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login, name='login'),
    path('login_check/', views.login_check, name='login_check'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('logout_user',views.logout_user,name='logout'),

    #staff
    path('addstaff/',views.addstaff, name='addstaff'),
    path('allstaff/', views.allstaff, name='allstaff'),
    path('store_staff', views.store_staff, name='store_staff'),
    path('edit_staff/<int:id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:id>', views.delete_staff, name='delete_staff'),
    path('update_staff/<int:id>/', views.update_staff, name='update_staff'),
    

    #client
    path('addclient/',views.addclient, name='addclient'),
    path('allclient/', views.allclient, name='allclient'),
    path('store_client', views.store_client, name='store_client'),
    path('delete_client/<int:id>', views.delete_client, name='delete_client'),

    #cases
    path('addcases/', views.addcases, name='addcases'),
    path('store_case', views.store_case, name='store_case'),
    path('view_cases/<int:id>/', views.view_cases, name='view_cases'),
    path('update_case/<int:id>', views.update_case, name='update_case'),
    path('allcases/', views.allcases, name='allcases'),
    path('edit_case/<int:id>/', views.edit_case, name='edit_case'),
    path('delete_case/<int:id>', views.delete_case, name='delete_case'),


    path('add_evidence/', views.add_evidence, name='add_evidence'),


    path('hearingdate/',views.all_dates ,name='hearingdate'),
    path('delete_hearing/<int:id>', views.delete_hearing, name='delete_hearing'),
    path('appointment/', views.appointment, name='appointment'),
    path('inquiries/', views.inquiries, name='inquiries'),
    path('delete_inquiries/<int:id>', views.delete_inquiries, name='delete_inquiries'),
    path('feedback/', views.feedback, name='feedback'),

    

]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    
     # for media files

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)