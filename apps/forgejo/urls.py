from django.urls import path
from .views import (
    ForgejoProfileView,
    ForgejoProfileCreateView,
    CreateRepositoryView,
    ListRepositoryView,
    UploadFileRepositoryView,
    UploadFileToForgejo,
    )


urlpatterns = [
    path('users/', ForgejoProfileCreateView.as_view()),
    path('users/<str:email>/', ForgejoProfileView.as_view()),
    path('users/<str:email>/repos/', CreateRepositoryView.as_view()),
    path('repos/<str:email>/<str:repo>/', ListRepositoryView.as_view()),
    path('repos/<str:email>/<str:repo>/contents/<str:filepath>/', UploadFileRepositoryView.as_view()),
    path('repos/<str:email>/<str:repo>/upload-file/', UploadFileToForgejo.as_view()),
]
