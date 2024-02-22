from django.urls import path
from directions import views


urlpatterns = [
    path("directions/", views.DirectionViewSet.as_view({'get': 'list'})),
    path("directions/<str:id>", views.DirectionViewSet.as_view({'get': 'retrieve'})),
    path("institute/", views.InstituteViewSet.as_view({'get': 'list'})),
    path("institute/<str:id>", views.InstituteViewSet.as_view({'get': 'retrieve'})),
    path("departments/", views.DepartmentViewSet.as_view({'get': 'list'})),
    path("departments/<int:id>", views.InstituteViewSet.as_view({'get': 'retrieve'})),
]