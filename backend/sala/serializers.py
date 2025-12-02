from rest_framework import serializers
from .models import Sala, SalaDeReuniao
from django.utils import timezone

class SalaSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Sala
        fields = [
            'id_sala',
            'nome_sala',
            'tipo_sala',
            'status',
            'capacidade',
            'descricao',
            'planta',       #mostrar o id de planta
        ]
        read_only_fields = ['status']

    def get_status(self, obj):
        #implementação do status em tempo real
        #obj é a instancia da sala que será serializada

        agora = timezone.now()

        for reserva in obj.reservas.all():
            if(reserva.data_inicio <= agora and reserva.data_fim >= reserva.status == 'confirmada'):
                return 'ocupada'
        
        return 'desocupada'
    

class SalaDeReuniaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaDeReuniao
        fields = ['id', 'nome']