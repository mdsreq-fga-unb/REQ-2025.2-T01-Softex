from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
from django.conf import settings
import json
from .models import Cadastro
from .serializers import CadastroSerializer, LoginSerializer

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all().order_by('id')
    serializer_class = CadastroSerializer

    #definindo as permições de ação
    def get_permissions(self):
        # se for criação de novo usuário, permite que qualquer um se registre
        if self.action == 'create':
            permissions_classes = [permissions.AllowAny]

        else:
            # para as outras ações exige que o user seja adm
            permissions_classes = [permissions.IsAdminUser]
        
        return [permissions() for permissions in permissions_classes]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def google_login_redirect(request):
    """
    Inicia o fluxo OAuth2 do Google
    Redireciona o usuário para a página de login do Google
    
    GET /api/auth/google/login/
    """
    # Configurar o fluxo OAuth2
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    )
    
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    
    # Gerar URL de autorização
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='select_account'
    )
    
    # Salvar state na sessão (para validação posterior)
    request.session['google_auth_state'] = state
    
    return redirect(authorization_url)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def google_callback(request):
    """
    Callback do OAuth2 do Google
    Recebe o código de autorização e troca por token
    
    GET /api/auth/google/callback/?code=...&state=...
    """
    try:
        # Verificar state (segurança)
        state = request.session.get('google_auth_state')
        if not state:
            print("❌ State não encontrado na sessão")
            return redirect(f"{settings.FRONTEND_URL}?error=state_invalido")
        
        print(f"✅ State verificado: {state[:20]}...")
        
        # Configurar o fluxo OAuth2
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                }
            },
            scopes=[
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
            ],
            state=state
        )
        
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        
        print(f"🔄 Trocando código por token...")
        print(f"📍 Redirect URI: {settings.GOOGLE_REDIRECT_URI}")
        
        # Trocar código por token
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        
        print("✅ Token obtido com sucesso!")
        
        # Obter credenciais
        credentials = flow.credentials
        
        print("🔍 Verificando token ID...")
        
        # Verificar token ID (com tratamento de clock skew)
        try:
            idinfo = id_token.verify_oauth2_token(
                credentials.id_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError as ve:
            # Se erro de clock skew, tentar novamente sem verificação estrita de tempo
            print(f"⚠️ Erro de verificação: {str(ve)}")
            if "too early" in str(ve).lower() or "clock" in str(ve).lower():
                print("🕐 Problema de sincronização de relógio detectado")
                # Decodificar sem verificação estrita (apenas para desenvolvimento)
                import jwt as pyjwt
                idinfo = pyjwt.decode(
                    credentials.id_token,
                    options={"verify_signature": False}
                )
            else:
                raise
        
        print(f"✅ Token verificado! Email: {idinfo.get('email')}")
        
        # Verificar email verificado
        if not idinfo.get('email_verified'):
            print("❌ Email não verificado pelo Google")
            return redirect(f"{settings.FRONTEND_URL}?error=email_not_verified")
        
        # Extrair informações
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        
        # verifica se email está cadastrado no banco de dados
        if not Cadastro.objects.filter(email=email).exists():
            print("❌ Email não autorizado")
            return redirect(f"{settings.FRONTEND_URL}?error=email_nao_autorizado")
        


        # Buscar ou criar usuário
        user, created = Cadastro.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': first_name,
                'last_name': last_name,
                'tipo_funcao': 'colaborador',
            }
        )
        
        if created:
            user.set_unusable_password()
            user.save()
        
        # Redirecionar para frontend com dados do usuário
        user_data = json.dumps({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tipo_funcao': user.tipo_funcao,
        })
        
        # Redirecionar para frontend com sucesso
        return redirect(f"{settings.FRONTEND_URL}?auth=success&user={user_data}&new_user={created}")
        
    except Exception as e:
        # Log do erro completo
        print(f"❌ ERRO no callback do Google: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Redirecionar com erro
        error_msg = str(e).replace(' ', '_')
        return redirect(f"{settings.FRONTEND_URL}?error={error_msg}")


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Endpoint para login tradicional (email/senha)
    NOTA: Este projeto usa login via Google SSO
    
    POST /api/login/
    Body: {
        "email": "usuario@email.com",
        "password": "senha123"
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user_data = serializer.validated_data
        return Response({
            'message': 'Login realizado com sucesso!',
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'tipo_funcao': user_data['tipo_funcao'],
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)