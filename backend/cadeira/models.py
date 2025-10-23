from django.db import models
from planta.models import Planta

class Cadeira(models.Model):
    TIPO_STATUS_CHOICES = [
        ('ocupado', 'Ocupado'),
        ('livre', 'Livre'),
    ]
    
    id_cadeira = models.AutoField(primary_key=True)
    planta= models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='cadeiras')
    status = models.CharField(max_length=10, choices=TIPO_STATUS_CHOICES, default='Livre')

    def __str__(self):
        return f"Cadeira_id: {self.id_cadeira}\n Status: {self.status}\n Planta: {self.planta}\n"