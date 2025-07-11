from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from rest_framework.routers import DefaultRouter
from service_category.views import CategoryListCreateView , CategoryDetailView,ServiceCreateView,ServiceDetailView,EmployeeRegisterView,EmployeeProfileView,EmployeeListView,EmployeeLoginView,BookingViewSet,EmployeeLogoutView

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
 

    path('category/', CategoryListCreateView.as_view(), name='category-detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('services/', ServiceCreateView.as_view(), name='category-detail'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='category-detail'),

    path('employees/register/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('employees/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employees/logout/', EmployeeLogoutView.as_view(), name='employee-logout'),
    path('employees/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += router.urls
