from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class ForgejoProfile(models.Model):
    '''Profile for students users'''
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, primary_key=True, unique=True)
    # forgejo_id = models.IntegerField(_('id in forgejo'), blank=True, null=True)
    username = models.CharField(_('username'), max_length=100, blank=True)
    repo_name = models.CharField(_('repository name'), max_length=150, blank=True, null=True)
    last_commit_id = models.CharField(_('last commit id'), max_length=256, blank=True, null=True)
    sha = models.CharField(_('sha'), max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = _('Профиль в forgejo')
        verbose_name_plural = _('Профили в forgejo')
