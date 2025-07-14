from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from . import views
# from rest_framework.routers import DefaultRouter
# from service.views import CategoryView,CategoryDetailView,ServicesListCreateView,ServicesDetailView,EmployeeRegisterView,EmployeeProfileView,EmployeeLoginView,EmployeeListView,BookingViewSet,EmployeeLogoutView


urlpatterns = [
 
 
    # path('category/', CategoryView.as_view(), name='category-detail'),


    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
 
]


