from django.shortcuts import render
from .models import Category,Services,Employee,Booking
from service_category.serializers import ServiceCategorySerializer,ServiceSerializer,EmployeeRegisterSerializer,EmployeeProfileSerializer,LoginSerializer,BookingSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser ,AllowAny
from rest_framework import generics,viewsets , permissions ,status
from django.shortcuts import get_object_or_404



class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser] 
    queryset = Category.objects.all()
    serializer_class = ServiceCategorySerializer
 
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser] 
    queryset = Category.objects.all()
    serializer_class = ServiceCategorySerializer

        
class ServiceCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

        
class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    
class EmployeeRegisterView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self,serializer):
        employee = serializer.save()
        employee.user.is_staff = True
        employee.user.save()

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
        
class EmployeeLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                try:
                    RefreshToken(token.token).blacklist()
                except TokenError:
                    continue

            return Response(
                {"detail": "Employee logged out successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Logout failed. Something went wrong."},
                status=status.HTTP_400_BAD_REQUEST
            )

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=user)
 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
 




