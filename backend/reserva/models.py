from django.db import models
from django.conf import settings
from sala.models import Sala
from cadastro.models import Cadastro

class Reserva(models.Model):
    STATUS_RESERVA_CHOICES = [
        ('confirmada','Confirmada'),
        ('cancelada','Cancelada'),
        # ainda podemos colocar como 'pendente' futuramente

    ]

    id_reserva = models.AutoField(primary_key=True)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # se usurário for deletado a reserva ainda fica, como forma de manter historico
        null=True, 
        related_name='reservas'
    )

    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE, # se a sala for deletada a reserva some
        related_name='reservas',
    )

    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_RESERVA_CHOICES, default='confirmada')


    data_criacao =  models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usuario_str = self.usuario.email if self.usuario else "Usuário Deletado"
        return(
            f"Reserva de {self.sala.nome_sala} por {usuario_str} [Status: {self.get_status_display()}]"
        )

    class Meta:
        db_table = 'reserva'
        ordering = ['data_inicio']