from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, generics, views, filters
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Student, Teacher
from . import serializers, services


def staff_required(view_func):
    def wrapped_view(view_instance, request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(view_instance, request, *args, **kwargs)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapped_view

@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"success": "CSRF cookie set"}, status=status.HTTP_200_OK)


# @method_decorator(csrf_protect, name="dispatch")
class UserRegisterView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request):
        try:
            attr = services.register(self, request)
            if attr:
                return Response({
                        'access': attr['access'],
                        'refresh': attr['refresh'],
                        'user': attr['user'].data,
                        'message': 'Registered successful'
                        }, status=status.HTTP_201_CREATED)
            return Response({'message': "Пользователь с такой почтой уже существует"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersListView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


# ==================== AUTH ====================
# @method_decorator(csrf_protect, name="dispatch")
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request):
        try:
            serializer = serializers.LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            if user:
                login_serializer = self.get_serializer(data=request.data)
                if login_serializer.is_valid():
                    # login(request, user)
                    user = services.get_role_view_serializer(data=user, role=user.role)
                    return Response({
                        'access': login_serializer.validated_data['access'],
                        'refresh': login_serializer.validated_data['refresh'],
                        'user': user.data,
                        'message': 'Login successful'
                        }, status=status.HTTP_200_OK)
            
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # logout(request)
            return Response({'success': _('You have been logged out.')}, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    allow_methods = ['GET']

    def get(self, request):
        try:
            user = request.user
            user_profile = User.objects.get(email=user.email)
            if user.role == User.Roles.TEACHER:
                user_profile = Teacher.objects.get(email=user.email)
                user_profile = serializers.TeacherSerializer(user_profile, many=False)
            elif user.role == User.Roles.STUDENT:
                user_profile = Student.objects.get(email=user.email)
                user_profile = serializers.StudentSerializer(user_profile, many=False)
            else:
                user_profile = serializers.AdminSerializer(user_profile, many=False)
            return Response(user_profile.data)
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited
    """
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows students to be viewed or edited
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']
