from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import PerfilDePermissao
from .serializers import PerfilPermissaoSerializer

class PerfilPermissaoViewSet(viewsets.ModelViewSet):
    # Garante que todos os perfis sejam listados e ordenados
    queryset = PerfilDePermissao.objects.all().order_by('id')
    serializer_class = PerfilPermissaoSerializer

    # Esta ação customizada lida com a lista completa enviada pelo Vue
    @action(detail=False, methods=['post'], url_path='update-all-profiles')
    def update_all_profiles(self, request):
        profiles_data = request.data  # Espera uma lista de objetos PerfilPermissao
        updated_profiles = []

        # Usamos transação atômica: se algo falhar, o DB reverte.
        with transaction.atomic():
            
            # 1. Identifica IDs existentes na submissão
            submitted_ids = [p.get('id') for p in profiles_data if p.get('id') is not None]
            
            # 2. Excluir perfis que existiam no DB, mas não vieram do Front (foram deletados visualmente)
            PerfilDePermissao.objects.exclude(id__in=submitted_ids).delete()

            # 3. Processar Atualizações e Criações
            for data in profiles_data:
                profile_id = data.get('id')
                
                if profile_id:
                    # Tenta atualizar (UPDATE)
                    try:
                        instance = PerfilDePermissao.objects.get(id=profile_id)
                        serializer = self.get_serializer(instance, data=data)
                    except PerfilDePermissao.DoesNotExist:
                        # Se o ID não existir (ID temporário do Front para um novo item)
                        serializer = self.get_serializer(data=data)
                else:
                    # Cria novo (CREATE) - o ID temporário do Front é ignorado aqui
                    serializer = self.get_serializer(data=data)

                # Valida e salva no banco de dados
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                updated_profiles.append(serializer.data)

        # Retorna a lista completa e atualizada para o Front
        return Response(updated_profiles, status=200)

