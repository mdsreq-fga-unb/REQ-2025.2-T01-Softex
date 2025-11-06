from django.db import models
from sala.models import Sala

class Cadeira(models.Model):
    STATUS_CHOICES = [
        ('ocupada', 'Ocupada'),
        ('desocupada', 'Desocupada'),
]

    id_cadeira = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='cadeiras')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='desocupada')
    
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)


    def __str__(self):
        return (f"Cadeira_id: {self.id_cadeira}\n"
                f"Status: {self.status}\n"
                f"sala: {self.sala.nome_sala}\n"
                f"Planta: {self.sala.planta.nome}\n")
    

    class Meta:
        db_table = 'cadeira'


    #=========================================================
    # validação de quantidade de cadeiras antes de salvar

    def save(self, *args, **kwargs):
        if not self.pk and self.sala:
            if self.sala.cadeiras.count() >= self.sala.capacidade:
                raise ValueError("A sala atingiu sua capacidade máxima de cadeiras.")
            
        super().save(*args, **kwargs)
        




