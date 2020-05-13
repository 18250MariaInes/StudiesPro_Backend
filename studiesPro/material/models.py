from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=80, null=True)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    provider = models.ForeignKey(
        'provider.Provider',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Material: {}'.format(self.name)

