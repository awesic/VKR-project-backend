from django.urls import path
from .views import (
    ThemePreferTeacherChangeView,
    AdminActionsView,
    TeacherPreferThemeChangeView,
    StudentsByTeacherView,
    StatusOptionsView
)

urlpatterns = [
    path("student/change/", ThemePreferTeacherChangeView.as_view()),
    path("<str:who>/<str:email>/change/", AdminActionsView.as_view()),
    path("teacher/student/<str:email>/change/", TeacherPreferThemeChangeView.as_view()),
    path("teacher/students-choose-list/", StudentsByTeacherView.as_view()),
    path("status/", StatusOptionsView.as_view()),
]