from rest_framework import serializers
from .models import Cadeira

#ao usar o model serializer a gente herda todos os campos da model, usando so o serializer, herda campos especificados
class CadeiraSerializer(serializers.ModelSerializer):
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Cadeira
        fields = [ 
            'id_cadeira',
            'sala',           
            'status',         
            'status_display', 
            'pos_x',          
            'pos_y',          
        ]

    def validate(self, data):
        sala = data['sala']
        if sala.cadeiras.count() >= sala.capacidade:
            raise serializers.ValidationError({"Sala": "Essa sala já está cheia. Não é possivel adicionar mais cadeiras"})
        return data