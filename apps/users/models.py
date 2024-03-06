import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .managers import UserManager
from apps.directions.models import Direction, Institute, Department


def year_validation(value):
    if value < datetime.datetime.now().year:
        raise ValidationError(_(f"{value} is not a correct year!"))


class User(AbstractUser):
    """
    Custom user model that supports using email instead of username and set ADMIN role ad default
    """

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Админ',
        TEACHER = 'teacher', 'Преподаватель',
        STUDENT = 'student', 'Студент'

    username = None
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    patronymic = models.CharField(_("patronymic"), max_length=150, blank=True)
    role = models.CharField(_("role"), max_length=50, choices=Roles.choices, default=Roles.ADMIN)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    @classmethod
    def _check_model(cls):
        errors = []
        return errors


class Teacher(User):
    """
    Custom teacher model that create teachers additional fields
    """
    
    institute = models.ForeignKey(Institute, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(
        Department, related_name='+', on_delete=models.SET_NULL, max_length=150, blank=True, null=True)
    

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.email}'


class Student(User):
    """
    Custom student model that create students additional fields
    """

    class Status(models.TextChoices):
        TOPIC_CHOICE = 'topic_choice', _('Выбор темы')
        THEORETICAL_ASPECTS = 'theoretical_aspects', _('Изучение теоретических аспектов темы')
        DATA_COLLECTION_AND_ANALYSIS = 'data_collection_and_analysis', _('Сбор и анализ данных')
        MAIN_WORK = 'main_wokr', _('Написание основной части / Разработка')
        DECORATION_FQW = 'decorator_fqw', _('Оформление ВКР')
        FINISHED = 'finished', _('Завершено')

    institute = models.ForeignKey(Institute, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    direction = models.ForeignKey(Direction, related_name='+', on_delete=models.SET_NULL, max_length=150,
                                  blank=True, null=True)
    group = models.CharField(_("group"), max_length=10, blank=True)
    graduate_year = models.PositiveSmallIntegerField(_("graduate year"),
                                                     validators=[year_validation], blank=True, null=True)
    prefer_teacher = models.ForeignKey(Teacher, related_name='+', on_delete=models.SET_NULL,
                                       blank=True, null=True)
    teacher_approved = models.BooleanField(_("teacher approved"), default=False)
    theme = models.CharField(_("theme"), max_length=150, blank=True)
    theme_approved = models.BooleanField(_("theme approved"), default=False)
    status = models.CharField(_("status"),
                              max_length=50, choices=Status.choices, default=Status.TOPIC_CHOICE, blank=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.email}'
