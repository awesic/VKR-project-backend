from django.db import models


class Institute(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    label = models.CharField(max_length=150)
    fullname = models.CharField(max_length=150)

    # objects = models.Manager()
    class Meta:
        verbose_name = 'Институт'
        verbose_name_plural = 'Институты'

    def __str__(self):
        return f"{self.label}"


class Direction(models.Model):
    id = models.CharField(max_length=8, unique=True, primary_key=True)
    label = models.CharField(max_length=150)
    institutes = models.ManyToManyField(Institute)

    # objects = models.Manager()
    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f"{self.id} - {self.label}"


class Department(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    label = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

    def __str__(self):
        return f"{self.label}"
    
    def get_label(self):
        return f"{self.label}"
