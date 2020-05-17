from django.db import models

class Semester(models.Model):
    beginning = models.DateField()
    end = models.DateField()
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Semester: {}'.format(self.end)

