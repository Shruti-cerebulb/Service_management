from django.contrib import admin
from django.urls import path,include
from user.views import RegisterView,UserProfileView,LoginView,DashboardView,UserListView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

 
 
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('dashboard/',DashboardView.as_view(), name="dashboard"),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    # path('user/', UserProfileView.as_view(), name='user-profile'),
 
 
 
 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
 
]