from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=80, null=True)
    description = models.CharField(max_length=200)
    date = models.DateField()
  

    def __str__(self):
        return 'Book: {}'.format(self.name)

