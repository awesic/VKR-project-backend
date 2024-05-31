from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics, views, status, exceptions
from rest_framework.response import Response

from apps.users.permissions import IsStudent, IsTeacher
from apps.users import models, serializers
from .services import map_status_list_to_json


class ThemePreferTeacherChangeView(generics.UpdateAPIView):
    """
    Change the theme and the prefer teacher by student
    """
    permission_classes = [IsStudent]
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()
    lookup_field = 'email'

    def get_object(self):
        try:
            instance = self.queryset.get(email=self.request.user)
            return instance
        except models.Student.DoesNotExist:
            raise exceptions.NotFound("Student")

    def put(self, request, *args, **kwargs):
        try:
            if 'theme_approved' not in request.data and 'teacher_approved' not in request.data:
                data = request.data.copy()
                if 'theme' in data:
                    data['theme_approved'] = False

                serializer = self.serializer_class(self.get_object(), data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"message": e.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminActionsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.StudentSerializer

    def put(self, request, *args, **kwargs):
        try:
            serializer = None
            if kwargs['who'] == 'student':
                obj = models.Student.objects.get(email=kwargs['email'])
                serializer = serializers.StudentSerializer(obj, data=request.data, partial=True)
            elif kwargs['who'] == 'teacher':
                obj = models.Teacher.objects.get(email=kwargs['email'])
                serializer = serializers.TeacherSerializer(obj, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        try:
            obj = models.User.objects.get(email=kwargs['email'])
            if obj:
                obj.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherPreferThemeChangeView(generics.UpdateAPIView):
    """
    Change the theme and the prefer teacher approvements of student by teacher
    """
    permission_classes = [IsTeacher]
    serializer_class = serializers.StudentSerializer

    def put(self, request, *args, **kwargs):
        try:
            obj = models.Student.objects.get(email=kwargs['email'])
            serializer = serializers.StudentSerializer(obj, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong teacher"}, status=status.HTTP_400_BAD_REQUEST)


class StatusOptionsView(views.APIView):
    """
    Returns a list of options for the student status.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        options = models.Student.Status.choices
        options = map_status_list_to_json(options)
        return Response(options, status=status.HTTP_200_OK)


class StudentsByTeacherView(generics.ListAPIView):
    permission_classes = [IsTeacher]
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        try:
            instance = self.queryset.filter(
                prefer_teacher=self.request.user.pk, 
                **self.request.query_params.dict()).order_by('-graduate_year')
            return instance
        except models.Student.DoesNotExist:
            raise exceptions.NotFound("Student")


