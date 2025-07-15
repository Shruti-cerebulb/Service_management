from rest_framework import generics , permissions ,status
# from django.contrib.auth.models import User
from service.serializers import UserProfileSerializer,RegisterSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs): 
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff and not user.is_superuser:
                return Response(
                    {'detail': 'Employees are not allowed to login here.'},
                    status=status.HTTP_403_FORBIDDEN
                )
 
            refresh = RefreshToken.for_user(user)
            user_serializer = UserProfileSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request, *args, **kwargs):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                try:
                    RefreshToken(token.token).blacklist()
                except TokenError:
                    continue
 
            return Response(
                {"detail": "User logged out successfully."},
                status=status.HTTP_200_OK
            )
 
        except Exception as e:
            return Response(
                {"detail": "Logout failed. Something went wrong."},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        user_serializer = UserProfileSerializer(user)
        return Response({
            'message' : 'welcome to service_hub',
            'user' : user_serializer.data
        }, 200)
    

class UserListView(ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Only return users who are NOT employees
        return CustomUser.objects.filter(employee_profile__isnull=True)
    



    
