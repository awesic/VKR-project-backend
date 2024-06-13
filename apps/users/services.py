from django.contrib.auth import login
from . import serializers
from .models import User, Student, Teacher
from apps.forgejo import services


def get_role_object_byEmail(email:str, role='admin'):
    user_profile = User.objects.get(email=email)
    if role.lower() == 'teacher':
        user_profile = Teacher.objects.get(email=email)
        user_profile = serializers.TeacherSerializer(user_profile, many=False)
    elif role.lower() == 'student':
        user_profile = Student.objects.get(email=email)
        user_profile = serializers.StudentSerializer(user_profile, many=False)
    else:
        user_profile = serializers.AdminSerializer(user_profile, many=False)
    
    return user_profile


def get_role_view_serializer(data=None, role='admin'):
    if role.lower() == 'student':
        data = serializers.StudentSerializer(data, many=False)
    elif role.lower() == 'teacher':
        data = serializers.TeacherSerializer(data, many=False)
    else:
        data = serializers.AdminSerializer(data, many=False)
        
    return data


def get_role_register_serializer(data=None):
    if str(data.get('role')).lower() == 'student':
        data = serializers.StudentRegisterSerializer(data=data)
    elif str(data.get('role')).lower() == 'teacher':
        data = serializers.TeacherRegisterSerializer(data=data)
    else:
        data = serializers.UserSerializer(data=data)
        
    return data


def register(self, request):
    serializer = get_role_register_serializer(data=request.data)
    attr = dict()

    if serializer.is_valid():
        attr['user'] = serializer.create(serializer.validated_data)
        try:
            forgejo_user = services.create_forgejo(request.data, user_id=attr['user'].pk)
            
            if attr:
                login_serializer = self.get_serializer(data=request.data)
                if login_serializer.is_valid():
                    login(request, attr['user'])
                    attr['user'] = get_role_view_serializer(data=attr['user'], role=attr['user'].role)
                    attr['access'] = login_serializer.validated_data['access']
                    attr['refresh'] = login_serializer.validated_data['refresh']
                    
                    return attr
        except Exception as e: raise
    return None
