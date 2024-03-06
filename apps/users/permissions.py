from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if str(request.user.role).lower() == 'student':
                return True
            else:
                return False
        else:
            return False


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if str(request.user.role).lower() == 'teacher':
                return True
        else:
            return False