from rest_framework import serializers

from sshipevent.models import Sshipevent
from students.serializers import StudentSerializer


class SshipeventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sshipevent
        fields = (
            'id',
            'name',
            'description',
            'hours',
            'date',
            'student'
        )

