from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Cadastro

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro 
        fields = [
            'id',
            'username',
            'email',
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


class LoginSerializer(serializers.Serializer):
    """Serializer para login de usuário"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Buscar usuário pelo email
            try:
                user = Cadastro.objects.get(email=email)
                # Verificar senha
                if user.check_password(password):
                    if not user.is_active:
                        raise serializers.ValidationError('Usuário desativado.')
                    return {
                        'user': user,
                        'email': user.email,
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'tipo_permissao': user.tipo_permissao,
                    }
                else:
                    raise serializers.ValidationError('Email ou senha incorretos.')
            except Cadastro.DoesNotExist:
                raise serializers.ValidationError('Email ou senha incorretos.')
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')
        
        return data
        