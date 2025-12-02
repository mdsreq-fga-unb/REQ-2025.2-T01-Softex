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
            'tipo_funcao',
            'password',
            'perfil',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # remove password e perfil do dict antes de criar o usuário
        password = validated_data.pop("password")
        perfil = validated_data.pop("perfil", None)

        # cria o usuário sem senha primeiro
        user = Cadastro(**validated_data)

        # aplica as permissões do perfil (se houver)
        if perfil:
            user.perfil = perfil
            user.acessoBasico = perfil.acessoBasico
            user.dashboards = perfil.dashboards
            user.salasReuniao = perfil.salasReuniao
            user.administracao = perfil.administracao

        # aplica a senha corretamente
        user.set_password(password)
        user.save()

        return user



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
                        'tipo_funcao': user.tipo_funcao,
                    }
                else:
                    raise serializers.ValidationError('Email ou senha incorretos.')
            except Cadastro.DoesNotExist:
                raise serializers.ValidationError('Email ou senha incorretos.')
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')
        
        return data
        