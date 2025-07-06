from rest_framework import generics
from django.contrib.auth.models import User
from service.serializers import RegisterSerializer, LoginSerializer , UserSerializer , UserProfileSerializer,ServiceCategorySerializer,ServiceSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Category,Services
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
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

class DashboardView(APIView):
    Permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message' : 'welcome to service_hub',
            'user' : user_serializer.data
        }, 200)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user()
        user.delete()
        return Response({"message": "User deleted"}, status=204)
    
class CategoryListCreateView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = ServiceCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Created!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CategoryDetailView(APIView):

    def get(self, request, pk):
        category_obj = get_object_or_404(Category, pk=pk)
        serializer = ServiceCategorySerializer(category_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        category_obj = get_object_or_404(Category, pk=pk)
        serializer = ServiceCategorySerializer(category_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated!", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category_obj = get_object_or_404(Category, pk=pk)
        category_obj.delete()
        return Response({"message": "Deleted!"}, status=status.HTTP_204_NO_CONTENT)
    
class ServiceCreateView(APIView):

    def get(self,request):
        service = Services.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Created!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ServiceDetailView(APIView):

    def get(self,request,pk):
        service = get_object_or_404(Services,pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)
    
    def put(self,request,pk):
        service = get_object_or_404(Services,pk=pk)
        serializer = ServiceSerializer(service,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Services Updated!","data":serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        service = get_object_or_404(Services,pk=pk)
        service.delete()
        return Response({'message':'Services Deleted!'},status=status.HTTP_204_NO_CONTENT)