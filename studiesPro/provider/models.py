from django.db import models

class Provider(models.Model):
    name = models.CharField(max_length=80, null=True)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=80)

    def __str__(self):
        return 'Provider: {}'.format(self.name)

