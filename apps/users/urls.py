from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView, 
    TokenVerifyView
)
from .views import (
    UsersListView,
    StudentViewSet,
    TeacherViewSet,
    ProfileView,
    UserRegisterView,
    LoginView,
    LogoutView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path('users/', UsersListView.as_view()),
    path('students/', StudentViewSet.as_view({'get': 'list'})),
    path('teachers/', TeacherViewSet.as_view({'get': 'list'})),
    path('profile/', ProfileView.as_view()),

    path('auth/register/', UserRegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    
    # JWT token
    path("auth/token/", CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
