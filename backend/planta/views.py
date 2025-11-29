from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from .models import Planta
from .serializers import PlantaSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    # Temporariamente permitir sem autenticação para desenvolvimento
    # TODO: Implementar autenticação por token para produção
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtrar plantas pelo usuário autenticado se necessário"""
        queryset = Planta.objects.all()
        user = self.request.user
        if user.is_authenticated:
            # Opcional: filtrar por usuário
            # queryset = queryset.filter(cadastro=user)
            pass
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Override create para adicionar logs detalhados"""
        print("\n" + "="*70)
        print("🌱 INICIANDO CRIAÇÃO DE PLANTA")
        print("="*70)
        print(f"📋 Método: {request.method}")
        print(f"🔗 URL: {request.path}")
        print(f"👤 Usuário: {request.user if request.user.is_authenticated else 'Anônimo'}")
        print(f"📦 Content-Type: {request.content_type}")
        print(f"📊 Dados recebidos:")
        
        # Log dos dados do request
        if request.FILES:
            print(f"   📎 Arquivos: {list(request.FILES.keys())}")
            for key, file in request.FILES.items():
                print(f"      - {key}: {file.name} ({file.size} bytes, {file.content_type})")
        
        if request.data:
            for key, value in request.data.items():
                if key == 'pontos':
                    try:
                        pontos = json.loads(value) if isinstance(value, str) else value
                        print(f"   📍 {key}: {len(pontos)} pontos")
                        for i, p in enumerate(pontos, 1):
                            print(f"      {i}. x={p.get('x')}%, y={p.get('y')}%")
                    except:
                        print(f"   📍 {key}: {value}")
                elif key != 'mapa_imagem':  # Já logado em FILES
                    print(f"   📝 {key}: {value}")
        
        print("-"*70)
        
        # Chamar método original
        response = super().create(request, *args, **kwargs)
        
        print("✅ PLANTA CRIADA COM SUCESSO!")
        if hasattr(response, 'data'):
            print(f"📤 Resposta: ID={response.data.get('id_planta')}, Nome={response.data.get('nome')}")
        print("="*70 + "\n")
        
        return response
    
    def update(self, request, *args, **kwargs):
        """Override update para adicionar logs detalhados"""
        print("\n" + "="*70)
        print("✏️  INICIANDO ATUALIZAÇÃO DE PLANTA")
        print("="*70)
        print(f"📋 Método: {request.method}")
        print(f"🔗 URL: {request.path}")
        print(f"🆔 ID da planta: {kwargs.get('pk')}")
        print(f"👤 Usuário: {request.user if request.user.is_authenticated else 'Anônimo'}")
        print(f"📦 Content-Type: {request.content_type}")
        print(f"📊 Dados recebidos:")
        
        # Log dos dados do request
        if request.FILES:
            print(f"   📎 Arquivos: {list(request.FILES.keys())}")
            for key, file in request.FILES.items():
                print(f"      - {key}: {file.name} ({file.size} bytes, {file.content_type})")
        
        if request.data:
            for key, value in request.data.items():
                if key == 'pontos':
                    try:
                        pontos = json.loads(value) if isinstance(value, str) else value
                        print(f"   📍 {key}: {len(pontos)} pontos")
                        for i, p in enumerate(pontos, 1):
                            print(f"      {i}. x={p.get('x')}%, y={p.get('y')}%")
                    except:
                        print(f"   📍 {key}: {value}")
                elif key != 'mapa_imagem':  # Já logado em FILES
                    print(f"   📝 {key}: {value}")
        
        print("-"*70)
        
        # Chamar método original
        response = super().update(request, *args, **kwargs)
        
        print("✅ PLANTA ATUALIZADA COM SUCESSO!")
        if hasattr(response, 'data'):
            print(f"📤 Resposta: ID={response.data.get('id_planta')}, Nome={response.data.get('nome')}")
        print("="*70 + "\n")
        
        return response
    
    def perform_create(self, serializer):
        """Associar o usuário autenticado à planta ao criar"""
        # Se usuário estiver autenticado, associar; senão criar sem usuário (para desenvolvimento)
        if self.request.user.is_authenticated:
            print(f"👤 Associando usuário {self.request.user.id} à planta")
            serializer.save(cadastro=self.request.user)
        else:
            # TODO: Em produção, criar um usuário padrão ou exigir autenticação
            print("⚠️ Usuário não autenticado - criando planta sem associar usuário")
            # Criar sem cadastro por enquanto (será necessário ajustar o model para permitir null)
            # Por enquanto, vamos precisar de um usuário padrão
            from cadastro.models import Cadastro
            default_user = Cadastro.objects.first()
            if default_user:
                serializer.save(cadastro=default_user)
                print(f"👤 Usando usuário padrão: {default_user.id}")
            else:
                # Se não houver usuários, criar um temporário
                print("❌ Nenhum usuário encontrado no banco!")
                print("⚠️ Tentando criar usuário padrão...")
                from cadastro.models import Cadastro
                # Criar usuário padrão se não existir
                default_user, created = Cadastro.objects.get_or_create(
                    email='admin@default.com',
                    defaults={
                        'username': 'admin_default',
                        'first_name': 'Admin',
                        'last_name': 'Default',
                        'tipo_permissao': 'admin',
                    }
                )
                if created:
                    default_user.set_password('admin123')  # Senha temporária
                    default_user.save()
                    print(f"✅ Usuário padrão criado: {default_user.id}")
                else:
                    print(f"👤 Usando usuário padrão existente: {default_user.id}")
                
                serializer.save(cadastro=default_user)

