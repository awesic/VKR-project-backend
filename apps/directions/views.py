from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from . import serializers
from .models import Direction, Institute, Department


class DirectionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Direction.objects.all()
    serializer_class = serializers.DirectionSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            direction = Direction.objects.filter(id=self.kwargs['id']).first()
            if direction:
                serializer = serializers.DirectionSerializer(direction)
                return Response(serializer.data)
            else:
                return Response({"message": "Direction not found"}, status=status.HTTP_404_NOT_FOUND)
        except Direction.DoesNotExist:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Institute.objects.all()
    serializer_class = serializers.InstituteSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            institute = Institute.objects.filter(id=self.kwargs['id']).first()
            if institute:
                serializer = serializers.InstituteSerializer(institute)
                return Response(serializer.data)
            else:
                return Response({"message": "Institute not found"}, status=status.HTTP_404_NOT_FOUND)
        except Institute.DoesNotExist:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            department = Department.objects.filter(id=self.kwargs['id']).first()
            if department:
                serializer = serializers.DepartmentSerializer(department)
                return Response(serializer.data)
            else:
                return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        except Department.DoesNotExist:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
