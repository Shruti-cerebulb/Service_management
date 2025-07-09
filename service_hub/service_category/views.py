from django.shortcuts import render
from .models import Category,Services,Employee,Booking
from service_category.serializers import ServiceCategorySerializer,ServiceSerializer,EmployeeRegisterSerializer,EmployeeProfileSerializer,LoginSerializer,BookingSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser ,AllowAny
from rest_framework import generics , permissions ,status
from django.shortcuts import get_object_or_404



class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self,request):
        categories = Category.objects.all()
        serializer = ServiceCategorySerializer(categories, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer= ServiceCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Created!","data":serializer.data},
                  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
    
class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        serializer = ServiceCategorySerializer(category_obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        serializer = ServiceCategorySerializer(category_obj, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Updated!","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        category_obj = get_object_or_404(Category,pk=pk)
        category_obj.delete()
        return Response({"message": "Deleted!"}, status=status.HTTP_204_NO_CONTENT)
        
class ServiceCreateView(APIView):
    permission_classes = [IsAdminUser]


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
    permission_classes = [IsAdminUser]


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
    
class EmployeeRegisterView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [AllowAny]

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [IsAdminUser]

class EmployeeProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.employee_profile
    
class EmployeeLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

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
        

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
class AllBookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]


