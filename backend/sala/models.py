from django.db import models
from planta.models import Planta

STATUS_CHOICES = [
    ('ocupada', 'Ocupada'),
    ('desocupada', 'Desocupa'),
]

class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    nome_sala = models.CharField(max_length=45)
    capacidade = models.IntegerField(default=0)
    status = models.CharField(max_length=45, choices=STATUS_CHOICES)
    descricao = models.CharField(blank=True, max_length=200)
    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE, related_name="salas"
    )

    def __str__(self):
        return f"Sala_id:{self.sala_id}\n Nome:{self.nome_sala}\n Capacidade:{self.capacidade}\n Status: {self.status}\n Planta_id:{self.planta_id}\n"
