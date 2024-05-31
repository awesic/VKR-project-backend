# Generated by Django 4.2.7 on 2024-03-29 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ForgejoProfile",
            fields=[
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("forgejo_id", models.BigIntegerField(verbose_name="id in forgejo")),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="username"
                    ),
                ),
                (
                    "repo_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="repository name",
                    ),
                ),
                (
                    "last_commit_id",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="last commit id",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль в forgejo",
                "verbose_name_plural": "Профили в forgejo",
            },
        ),
    ]