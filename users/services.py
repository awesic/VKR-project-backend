from django.contrib.auth import login, authenticate
from users import serializers


def register(request):
    serializer = serializers.UserSerializer(data=request.data)
    user = None
    # token = None
    if str(request.data.get('role')).lower() == 'student':
        serializer = serializers.StudentRegisterSerializer(data=request.data)

    elif str(request.data.get('role')).lower() == 'teacher':
        serializer = serializers.TeacherRegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)
#             user = serializers.UserSerializer(user)
    if user:
        user = authenticate(email=user.email, password=request.data.get('password'))
        login(request, user)
        if str(user.role).lower() == 'student':
            user = serializers.StudentSerializer(user, many=False)
        elif str(user.role).lower() == 'teacher':
            user = serializers.TeacherSerializer(user, many=False)
        else:
            user = serializers.AdminSerializer(user, many=False)

    return user