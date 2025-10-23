from django.db import models
from cadastro.models import Cadastro

class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='pantas')
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"Planta_id: {self.id_planta} \n Nome: {self.nome}\n Cadastro_id: {self.cadastro.id_cadastro}\n"
