# Generated by Django 4.2.7 on 2024-05-31 20:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="group",
            field=models.CharField(blank=True, max_length=20, verbose_name="group"),
        ),
    ]