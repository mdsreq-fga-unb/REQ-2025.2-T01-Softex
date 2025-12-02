from rest_framework import serializers
from .models import Reserva, ReservaCadeira

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva 
        fields = '__all__'


class ReservaCadeiraSerializer(serializers.ModelSerializer):
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    usuario_nome = serializers.SerializerMethodField()
    cadeira_id = serializers.IntegerField(source='cadeira.id_cadeira', read_only=True)
    
    class Meta:
        model = ReservaCadeira
        fields = [
            'id_reserva_cadeira',
            'usuario',
            'usuario_email',
            'usuario_nome',
            'cadeira',
            'cadeira_id',
            'data_inicio',
            'data_fim',
            'hora_inicio',
            'hora_fim',
            'status',
            'data_criacao',
            'data_modificacao',
        ]
        read_only_fields = ['usuario', 'data_criacao', 'data_modificacao']
    
    def get_usuario_nome(self, obj):
        if obj.usuario:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
        return None