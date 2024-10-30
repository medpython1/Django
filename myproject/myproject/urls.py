"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import path
from myapp import views



# urlpatterns = [
#     path('books/', views.book_list, name='book_list'),
#     path('books/<int:book_id>/', views.book_detail, name='book_detail'),
#     path('books/author/<str:author_name>/', views.books_by_author, name='books_by_author'),
# ]
# urlpatterns = [
#     path('book/<int:id>/', views.book_detail, name='book_detail'),
#     path('search/', views.book_detail_redirect, name='book_detail_redirect'),
# ]
# urlpatterns = [
#     path('add-book/', views.add_book, name='add_book'),
#     path('book/<str:id_number>/', views.get_book_by_id_number, name='get_book_by_id_number'),
#     path('book_detail/', views.book_list, name='books_by_author'),
# ]


# # myapp/urls.py
# from django.urls import path

# urlpatterns = [
    
#     path('book/<int:id>/', views.book_detail, name='book_detail'),  # Existing URL pattern
# ]
##########################################05-09-2024###########################
# urls.py
from django.urls import path
from myapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('vendor_master/', views.vendor_master, name='vendor_master'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('bill_generate/', views.bill_generate, name='bill_generate'),
    path('get_bill_list/', views.get_bill_list, name='get_bill_list'),
    path('generate_bill/', views.bill_generate, name='bill_generate'),
    path('bill_generate_qua/', views.bill_generate_qua, name='bill_generate_qua'),
    path('get_bill_list_qua/', views.get_bill_list_qua, name='get_bill_list_qua'),
    path('view_pdf/<str:pdf_file_name>/', views.view_pdf, name='view_pdf'),
    # path('view_pdf/<str:pdf_file_name>/', views.view_pdf_qua, name='view_pdf_qua'),
    
    path('view_pdf_qua/<str:pdf_file_name>/', views.view_pdf_qua, name='view_pdf_qua'),
    path('login/', views.login_view, name='login'),
    path('', lambda request: redirect('login'), name='root'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_and_list_view, name='register'),
     path('vendors/toggle/<str:vendor_id>/', views.toggle_vendor_status, name='toggle_vendor_status'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#     path('add-book/', search_api, name='add-book'),
# ]