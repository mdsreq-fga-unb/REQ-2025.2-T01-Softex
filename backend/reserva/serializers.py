from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time
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
    
    def validate(self, data):
        """
        Valida se não há conflito com reservas existentes
        """
        cadeira = data.get('cadeira')
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')
        hora_inicio = data.get('hora_inicio')
        hora_fim = data.get('hora_fim')
        
        if not all([cadeira, data_inicio, data_fim, hora_inicio, hora_fim]):
            return data
        
        # Converter hora_inicio e hora_fim para objetos time se forem strings
        if isinstance(hora_inicio, str):
            try:
                if len(hora_inicio.split(':')) == 3:
                    hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
                else:
                    hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            except ValueError:
                raise serializers.ValidationError({'hora_inicio': 'Formato de horário inválido'})
        
        if isinstance(hora_fim, str):
            try:
                if len(hora_fim.split(':')) == 3:
                    hora_fim = datetime.strptime(hora_fim, '%H:%M:%S').time()
                else:
                    hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
            except ValueError:
                raise serializers.ValidationError({'hora_fim': 'Formato de horário inválido'})
        
        # Buscar reservas confirmadas para esta cadeira
        reservas_existentes = ReservaCadeira.objects.filter(
            cadeira=cadeira,
            status='confirmada'
        ).exclude(
            pk=self.instance.pk if self.instance else None
        )
        
        # Verificar conflitos de horário
        for reserva in reservas_existentes:
            # Verificar se as datas se sobrepõem
            # Conflito de datas: data_inicio <= reserva.data_fim AND data_fim >= reserva.data_inicio
            datas_sobrepoem = data_inicio <= reserva.data_fim and data_fim >= reserva.data_inicio
            
            if datas_sobrepoem:
                # Se as datas se sobrepõem, verificar conflito de horário
                # Como as reservas são para um único dia (data_inicio == data_fim), 
                # só precisamos verificar conflito de horário se for o mesmo dia
                if data_inicio == reserva.data_inicio:
                    # Mesmo dia: verificar se os horários se sobrepõem
                    # Conflito de horários: hora_inicio < reserva.hora_fim AND hora_fim > reserva.hora_inicio
                    horarios_sobrepoem = hora_inicio < reserva.hora_fim and hora_fim > reserva.hora_inicio
                    
                    if horarios_sobrepoem:
                        usuario_reserva = reserva.usuario
                        nome_reserva = f"{usuario_reserva.first_name} {usuario_reserva.last_name}".strip() if usuario_reserva else "Usuário desconhecido"
                        
                        mensagem = (
                            f"Esta cadeira já está reservada no horário {reserva.hora_inicio.strftime('%H:%M')} "
                            f"até {reserva.hora_fim.strftime('%H:%M')} no dia {reserva.data_inicio}. "
                            f"Reservado por: {nome_reserva}"
                        )
                        raise serializers.ValidationError({'non_field_errors': [mensagem]})
        
        return data