from django.db import models

class Semester(models.Model):
    beginning = models.DateField()
    end = models.DateField()

    def __str__(self):
        return 'Semester: {}'.format(self.end)

