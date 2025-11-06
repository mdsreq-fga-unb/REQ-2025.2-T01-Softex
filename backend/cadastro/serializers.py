from rest_framework import serializers
from .models import Cadastro

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro 
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'tipo_permissao',
            'password'          #write_only
        ]

        extra_kwargs = {
            'password': {'write_only':True}
        }

        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)

            if password:
                instance.set_password(password)

            instance.save()
            return instance
        