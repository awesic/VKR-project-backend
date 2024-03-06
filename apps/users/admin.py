from django.contrib import admin

from .models import User, Student, Teacher


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     add_fieldsets = (
#         (None, {
#             'fields': ('email', 'password1', 'password2', 'role')
#         }),
#         ('Permissions', {
#             'fields': ('is_superuser', 'is_staff')
#         })
#     )
#     fieldsets = (
#         (None, {
#             'fields': ('email', 'password', 'role', 'first_name', 'last_name', 'patronymic')
#         }),
#         ('Permissions', {
#             'fields': ('is_superuser', 'is_staff')
#         })
#     )
#     list_display = ['email', 'role']
#     search_fields = ('email',)
#     ordering = ('email',)

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
