"""
URL configuration for service_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from service.views import RegisterView , LoginView , DashboardView, UserProfileView,CategoryDetailView,CategoryListCreateView,ServiceCreateView,ServiceDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('service.urls')),

    path('api/auth/register/',RegisterView.as_view(), name="auth_register"),
    path('api/auth/login/',LoginView.as_view(), name="auth_login"),
    path('api/dashboard/',DashboardView.as_view(), name="dashboard"),
    path('user/', UserProfileView.as_view(), name='user-profile'),

    path('category/', CategoryListCreateView.as_view(), name='category-detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('services/', ServiceCreateView.as_view(), name='category-detail'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='category-detail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
