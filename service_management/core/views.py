from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer,ProfileSerializer,CategorySerializer,ServiceSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ServiceCategory,Service
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly




class RegisterView(generics.CreateAPIView):
    user  = User.objects.all()
    serializer_class = RegisterSerializer
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(Self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                 'refresh' : str(refresh),
                 'access' : str(refresh.access_token),
                 'user' : user_serializer.data
            })
        else:
            return Response ({'detail' : 'invaild credentials'}, status=401)
        
class Dashboard(APIView):
    Permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message' : 'Welcome to Dashboard',
            'user' : user_serializer.data
        },200)
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access

    def get(self, request):
        user = request.user  # Get the current logged-in user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,id):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            "message": "User account deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)
        
        
class CategoryView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = CategorySerializer
    
    
class CategoryDetailView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        category_obj = get_object_or_404(ServiceCategory, pk=pk)
        serializer = CategorySerializer(category_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        category_obj = get_object_or_404(ServiceCategory, pk=pk)
        serializer = CategorySerializer(category_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated!", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category_obj = get_object_or_404(ServiceCategory, pk=pk)
        category_obj.delete()
        return Response({"message": "Deleted!"}, status=status.HTTP_204_NO_CONTENT)
    
    
class ServiceView(APIView):
    def get(self,request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ServiceSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Service created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceDetailView(APIView):
    def get(self,request,pk):
        services = get_object_or_404(Service,pk=pk)
        serializer = ServiceSerializer(services)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        services = get_object_or_404(Service,pk=pk)
        serializer = ServiceSerializer(services,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Service updated successfully!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def delete(self,request,pk):
        services = get_object_or_404(Service,pk=pk)
        services.delete()
        return Response({
            "message":"Deleted Succesfully"      
        },status=status.HTTP_204_NO_CONTENT)
               

    
    
            
        
    