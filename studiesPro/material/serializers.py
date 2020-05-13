from rest_framework import serializers

from material.models import Material
from provider.serializers import ProviderSerializer
from students.serializer import StudentSerializer

class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = (
            'id',
            'name',
            'description',
            'price',
            'provider',
            'student'
        )
