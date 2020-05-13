from django.db import models

class Sshipevent(models.Model):
    name = models.CharField(max_length=80, null=True)
    description = models.CharField(max_length=200)
    hours = models.PositiveIntegerField()
    date = models.DateField()
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Sshipevent: {}'.format(self.name)

