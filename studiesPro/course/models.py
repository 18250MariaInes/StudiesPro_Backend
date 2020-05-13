from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=80, null=True)
    teacher = models.ForeignKey(
        'teacher.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    semester = models.ForeignKey(
        'semester.Semester',
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
        return 'Course: {}'.format(self.name)
