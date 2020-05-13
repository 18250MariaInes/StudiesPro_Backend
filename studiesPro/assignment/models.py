from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=80, null=True)
    description = models.CharField(max_length=200)
    deadline = models.DateField()
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        'course.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Assignment: {}'.format(self.title)

