from rest_framework import serializers

from students.models import Student
#from parents.serializer import ParentSerializer

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'lastname',
            'carne',
            'sship',
            'email',
            'password'
        )
        extra_kwargs = {
				'password': {'write_only': True},
		}

    def save(self):
        student = Student(
            email=self.validated_data['email'])
        password = self.validated_data['password']
        student.set_password(password)
        student.save()
        return student