from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from service.views import CategoryView,CategoryDetailView,ServicesListCreateView,ServicesDetailView,EmployeeRegisterView,EmployeeProfileView,EmployeeLoginView,EmployeeListView,BookingView,BookingList,BookingDetailView
urlpatterns = [
 
 
    path('category/', CategoryView.as_view(), name='category-detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
 
    path('services/', ServicesListCreateView.as_view(), name='category-detail'),
    path('services/<int:pk>/', ServicesDetailView.as_view(), name='category-detail'),
    
    path('employee/register/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('employee/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
 

    path('booking/', BookingView.as_view(), name='booking-create'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
]