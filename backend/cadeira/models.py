from django.db import models
from sala.models import Sala

class Cadeira(models.Model):
    STATUS_CHOICES = [
        ('ocupada', 'Ocupada'),
        ('desocupada', 'Desocupada'),
]

    id_cadeira = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='cadeiras', default='Livre',choices=STATUS_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Livre')

    def __str__(self):
        return (f"Cadeira_id: {self.id_cadeira}\n"
                f" Status: {self.status}\n"
                f"Planta: {self.planta}\n")
    class Meta:
        db_table = 'cadeira'


    #=========================================================
    # validação de quantidade de cadeiras antes de salvar

    def salvar_cadeiras(self, *args, **kwargs):
        if self.sala.cadeiras.count() >= self.sala.capacidade:
            raise ValueError("A sala atingiu sua capacidade máxima de cadeiras.")
        super().save(args, **kwargs)
        




