from django.db import models

class Provider(models.Model):
    name = models.CharField(max_length=80, null=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(verbose_name="email", max_length=60, default="tettsa@gmail.com")

    def __str__(self):
        return 'Provider: {}'.format(self.name)

