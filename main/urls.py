from django.urls import path
from main import views

urlpatterns = [
    path("student/change/", views.ThemePreferTeacherChangeView.as_view()),
    path("<str:who>/<str:email>/change/", views.AdminActionsView.as_view()),
    path("teacher/student/<str:email>/change/", views.TeacherPreferThemeChangeView.as_view()),
    path("teacher/students-choose-list/", views.StudentsByTeacherView.as_view()),
    path("status", views.StatusOptionsView.as_view()),
]