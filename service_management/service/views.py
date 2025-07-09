from django.shortcuts import render
from .models import Category,Services,Employee,Booking
from service.serializers import CategorySerializer,ServicesSerializer,EmployeeRegisterSerializer,EmployeeProfileSerializer,EmployeeLoginSerializer,BookingSerializer
from rest_framework import generics,permissions,status
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


class CategoryView(APIView):
    permission_classes =[IsAdminUser]
    
    def get(self,request):
        category = Category.objects.all()
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Service created Succesfully',
                'data' :    serializer.data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailView(APIView):
    permission_classes =[IsAdminUser]
    def get(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category_obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category_obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Category Updated Succesfully',
                'data' : serializer.data
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        category_obj.delete()
        return Response({
            'message' : 'Deleted Succesfully',
        },status=status.HTTP_204_NO_CONTENT)
        
class ServicesListCreateView(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class ServicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    
class EmployeeRegisterView(generics.ListCreateAPIView):    
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [AllowAny]
    
class EmployeeProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]
 
    def get_object(self):
        return self.request.user.employee_profile
    
class EmployeeLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmployeeLoginSerializer
 
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
 
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
 
            try:
                employee = user.employee_profile
                employee_serializer = EmployeeProfileSerializer(employee)
                response_data['employee'] = employee_serializer.data
            except Employee.DoesNotExist:
               
                if not user.is_staff and not user.is_superuser:
                    return Response(
                        {'detail': 'User is not registered as an employee'},
                        status=status.HTTP_403_FORBIDDEN
                    )
 
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [IsAdminUser]
    
class BookingView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
class BookingList(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]
    
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Booking updated successfully ✅",
            "data": response.data
        }, status=status.HTTP_200_OK)
    
    
    
    
    
    

    

    



