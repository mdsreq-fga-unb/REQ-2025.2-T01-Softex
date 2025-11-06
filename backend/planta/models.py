from django.db import models
from django.conf import settings

class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    cadastro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pantas')
    
    nome = models.CharField(max_length=50)
    
    mapa_imagem = models.ImageField(
        upload_to='mapas_plantas/',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f"Planta_id: {self.id_planta}\n" 
                f"Nome: {self.nome}\n"
                f"Cadastro_id: {self.cadastro.id}\n")

    class Meta:
        db_table = 'planta'