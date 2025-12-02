# Generated manually to add perfil and boolean fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_alter_cadastro_tipo_funcao'),
        ('permissoes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro',
            name='perfil',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='usuarios',
                to='permissoes.perfildepermissao',
                verbose_name='Perfil de Acesso'
            ),
        ),
        migrations.AddField(
            model_name='cadastro',
            name='acessoBasico',
            field=models.BooleanField(default=True, verbose_name='Acesso Básico'),
        ),
        migrations.AddField(
            model_name='cadastro',
            name='dashboards',
            field=models.BooleanField(default=False, verbose_name='Dashboards'),
        ),
        migrations.AddField(
            model_name='cadastro',
            name='salasReuniao',
            field=models.BooleanField(default=False, verbose_name='Salas de Reunião'),
        ),
        migrations.AddField(
            model_name='cadastro',
            name='administracao',
            field=models.BooleanField(default=False, verbose_name='Administração'),
        ),
    ]

