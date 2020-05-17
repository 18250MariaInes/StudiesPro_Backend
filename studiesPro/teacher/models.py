from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=80, null=True)
    lastname = models.CharField(max_length=80, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    def __str__(self):
        return self.name

