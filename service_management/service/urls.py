from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from rest_framework.routers import DefaultRouter
from service.views import CategoryView,CategoryDetailView,ServicesListCreateView,ServicesDetailView,EmployeeRegisterView,EmployeeProfileView,EmployeeLoginView,EmployeeListView,BookingViewSet,EmployeeLogoutView




urlpatterns = [
 
 
    path('category/', CategoryView.as_view(), name='category-detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
 
    path('services/', ServicesListCreateView.as_view(), name='category-detail'),
    path('services/<int:pk>/', ServicesDetailView.as_view(), name='category-detail'),
    
    path('employee/register/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('employee/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/logout/', EmployeeLogoutView.as_view(), name='employee-login'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
 
]
router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
urlpatterns += router.urls

