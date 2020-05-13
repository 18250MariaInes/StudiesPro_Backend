from django.db import models

class Delvas(models.Model):
    name = models.CharField(max_length=80, null=True)
    date = models.DateField()
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Delvas: {}'.format(self.name)

