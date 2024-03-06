from django.urls import path
from .views import (
    DirectionViewSet,
    InstituteViewSet,
    DepartmentViewSet,
)


urlpatterns = [
    path("directions/", DirectionViewSet.as_view({'get': 'list'})),
    path("directions/<str:id>/", DirectionViewSet.as_view({'get': 'retrieve'})),
    path("institute/", InstituteViewSet.as_view({'get': 'list'})),
    path("institute/<str:id>/", InstituteViewSet.as_view({'get': 'retrieve'})),
    path("departments/", DepartmentViewSet.as_view({'get': 'list'})),
    path("departments/<int:id>/", InstituteViewSet.as_view({'get': 'retrieve'})),
]