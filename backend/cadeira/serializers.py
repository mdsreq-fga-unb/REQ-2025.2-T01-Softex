from rest_framework import serializers
from .models import Cadeira

#ao usar o model serializer a gente herda todos os campos da model, usando so o serializer, herda campos especificados
class CadeiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadeira
        fields = '__all__'