from django.db import models
from planta.models import Planta

TIPO_SALA_CHOICES = [
    ('estacao', 'Estação de Trabalho'),
    ('reuniao', 'Sala de Reunião'),
]

class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_SALA_CHOICES, default='estacao')
    
    nome_sala = models.CharField(max_length=45)
    capacidade = models.IntegerField(default=0)
    #status = models.CharField(max_length=45, choices=STATUS_CHOICES)
    descricao = models.CharField(blank=True, max_length=200)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name="salas")


    def __str__(self):
        tipo_display = self.get_tipo_display()
        return (
            f"Sala_id: {self.id_sala}\n"
            f"Tipo: {tipo_display}\n"
            f"Nome: {self.nome_sala}\n"
            f"Capacidade: {self.capacidade}\n"
            f"Planta_id: {self.planta.id_planta}\n"
        )

    class Meta:
        db_table = 'sala'


class SalaDeReuniao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'sala_de_reuniao'
        verbose_name = "Sala de Reunião (simples)"
        verbose_name_plural = "Salas de Reunião (simples)"