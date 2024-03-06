from django.urls import path

from .views import (
    UsersListView,
    StudentViewSet,
    TeacherViewSet,
    ProfileView,
    GetCSRFToken,
    UserRegisterView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('users/', UsersListView.as_view()),
    path('students/', StudentViewSet.as_view({'get': 'list'})),
    path('teachers/', TeacherViewSet.as_view({'get': 'list'})),
    path('account/profile/', ProfileView.as_view()),

    path('csrf_cookie', GetCSRFToken.as_view()),
    # path('auth/student/register', StudentRegisterView.as_view()),
    # path('auth/teacher/register', TeacherRegisterView.as_view()),
    path('auth/register/', UserRegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]
