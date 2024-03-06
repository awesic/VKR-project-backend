from rest_framework import serializers

from .models import Direction, Institute, Department


class DirectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direction
        fields = '__all__'


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'