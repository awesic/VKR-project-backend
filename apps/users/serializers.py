from typing import Any, Dict
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Student, Teacher


class UserSerializer(serializers.ModelSerializer):
    """
    Default Serializer for user model
    """
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'}, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'password', 'password2', 'role']
        read_only_fields = ['role']

    def validate(self, attrs):
        if attrs['password']!= attrs['password2']:
            raise serializers.ValidationError(_("Пароли не совпадают."))
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(_("Пользователь с таким email уже существует."))
        return attrs

    def create(self, validated_data):
        admin = User.objects.create_superuser(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic']
        )
        admin.set_password(validated_data['password'])
        admin.save()

        return admin


class AdminSerializer(serializers.ModelSerializer):
    """
    Serializer for show admin user
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'role']


class TeacherRegisterSerializer(serializers.ModelSerializer):
    """
    TeacherRegisterSerializer for the user create a new teacher user and token for authentication
    """
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'}, required=True, validators=[validate_password])  
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'patronymic',
                  'password', 'password2', 'institute', 'department']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": _("Пароли не совпадают.")})
        if Teacher.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(_("Такой пользователь уже существует."), code="authorization")
        return attrs

    def create(self, validated_data):
        teacher = Teacher.objects.create_user(
            email=validated_data['email']
            , password=validated_data['password']
            , first_name=validated_data['first_name']
            , last_name=validated_data['last_name']
            , patronymic=validated_data['patronymic']
            , institute=validated_data['institute']
            , department=validated_data['department']
            , role='teacher'
        )
        teacher.set_password(validated_data['password'])
        teacher.save()
        teacher = authenticate(email=validated_data['email'], password=validated_data['password'])
        return teacher


class StudentRegisterSerializer(serializers.ModelSerializer):
    """
    StudentRegisterSerializer for the user create a new student user and token for authentication
    """
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'}, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'patronymic',
                  'password', 'password2', 'institute', 'direction', 'group', 'graduate_year']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(_("Пароли не совпадают."), code="authorization")
        if Student.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(_("Такой пользователь уже существует."), code="authorization")
        return attrs

    def create(self, validated_data):
        student = Student.objects.create_user(
            email=validated_data['email']
            , password=validated_data['password']
            , first_name=validated_data['first_name']
            , last_name=validated_data['last_name']
            , patronymic=validated_data['patronymic']
            , institute=validated_data['institute']
            , direction=validated_data['direction']
            , group=validated_data['group']
            , graduate_year=validated_data['graduate_year']
            , role='student'
        )
        student.set_password(validated_data['password'])
        student.save()
        student = authenticate(email=validated_data['email'], password=validated_data['password'])
        return student


class LoginSerializer(serializers.ModelSerializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(label=_('email'), required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, trim_whitespace=False)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                msg = _('Не правильная почта или пароль.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Почта и пароль обязательны.')
            raise serializers.ValidationError(msg, code="authorization")
        attrs['user'] = user
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    fio = serializers.CharField(source='get_full_name', read_only=True)
    teacher_email = serializers.EmailField(source='prefer_teacher.email', read_only=True, allow_blank=True)
    teacher_fullname = serializers.CharField(source='prefer_teacher.get_full_name', read_only=True, allow_blank=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True, allow_blank=True)

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'fio',
                  'institute', 'direction', 'group', 'graduate_year',
                  'theme', 'theme_approved', 'prefer_teacher', 'teacher_email', 'teacher_fullname', 'teacher_approved',
                  'status', 'status_label', 'role']


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic',
                  'institute', 'direction', 'graduate_year',
                  'theme', 'theme_approved', 'prefer_teacher', 'teacher_approved', 'status', 'role']


class TeacherSerializer(serializers.ModelSerializer):
    fio = serializers.CharField(source='get_full_name', read_only=True)
    department_label = serializers.CharField(source='department.get_label', read_only=True, allow_blank=True)

    class Meta:
        model = Teacher
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'fio', 'institute', 'department', 'department_label', 'role']
        

# ==================== AUTH ====================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # return a dictionary data with keys "access" and "refresh"
    username_field = 'email'
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }
        user = authenticate(**credentials)
        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed(_('Пользователь диактивирован!'))
            
            data = {}
            refresh = self.get_token(user)
            
            data['access'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
            return data
        raise exceptions.AuthenticationFailed(_('Не найдено активных пользователей с заданными учетными данными!'))