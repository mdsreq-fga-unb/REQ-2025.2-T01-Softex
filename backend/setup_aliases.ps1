# ========================================
# Script para Configurar Aliases do Django
# ========================================
# Este script adiciona atalhos úteis ao seu PowerShell profile
#
# Uso: .\setup_aliases.ps1

Write-Host "🔧 Configurando aliases do Django no PowerShell..." -ForegroundColor Cyan
Write-Host ""

# Caminho do profile do PowerShell
$profilePath = $PROFILE

# Criar diretório do profile se não existir
$profileDir = Split-Path -Parent $profilePath
if (-Not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

# Verificar se o conteúdo já existe
if (Test-Path $profilePath) {
    $currentContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
    if ($currentContent -like "*Aliases Django - Backend Softex*") {
        Write-Host "⚠️  Aliases já estão configurados no profile!" -ForegroundColor Yellow
        Write-Host ""
        $response = Read-Host "Deseja sobrescrever? (S/N)"
        if ($response -ne "S" -and $response -ne "s") {
            Write-Host "❌ Operação cancelada." -ForegroundColor Red
            exit
        }
        
        # Remover seção antiga
        Write-Host "🔄 Removendo configuração antiga..." -ForegroundColor Yellow
        $newContent = $currentContent -replace "(?s)# ========================================\s*# Aliases Django - Backend Softex.*?Write-Host.*Aliases Django carregados.*\n", ""
        Set-Content -Path $profilePath -Value $newContent
    }
}

# Adicionar aliases ao profile linha por linha
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# ========================================"
Add-Content -Path $profilePath -Value "# Aliases Django - Backend Softex"
Add-Content -Path $profilePath -Value "# ========================================"
Add-Content -Path $profilePath -Value ("# Gerado automaticamente em " + (Get-Date -Format "yyyy-MM-dd HH:mm"))
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Caminho do projeto (AJUSTE SE NECESSÁRIO)"
Add-Content -Path $profilePath -Value '$DJANGO_PROJECT_PATH = "C:\Users\Felipe Pedroza\Documents\UnB\REQ-2025.2-T01-Softex\backend"'
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Ativar ambiente virtual (vv)"
Add-Content -Path $profilePath -Value "function vv {"
Add-Content -Path $profilePath -Value '    Write-Host "📦 Ativando ambiente virtual..." -ForegroundColor Yellow'
Add-Content -Path $profilePath -Value '    if (Test-Path "$DJANGO_PROJECT_PATH\venv\Scripts\Activate.ps1") {'
Add-Content -Path $profilePath -Value '        Push-Location $DJANGO_PROJECT_PATH'
Add-Content -Path $profilePath -Value '        & "$DJANGO_PROJECT_PATH\venv\Scripts\Activate.ps1"'
Add-Content -Path $profilePath -Value '        Write-Host "✅ Ambiente virtual ativado!" -ForegroundColor Green'
Add-Content -Path $profilePath -Value '        Write-Host "📁 Diretório: $DJANGO_PROJECT_PATH" -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value '    } else {'
Add-Content -Path $profilePath -Value '        Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red'
Add-Content -Path $profilePath -Value '        Write-Host "Crie com: python -m venv venv" -ForegroundColor Yellow'
Add-Content -Path $profilePath -Value '    }'
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Ir para o diretório do backend (cdb)"
Add-Content -Path $profilePath -Value "function cdb {"
Add-Content -Path $profilePath -Value '    Set-Location $DJANGO_PROJECT_PATH'
Add-Content -Path $profilePath -Value '    Write-Host "📁 Backend: $DJANGO_PROJECT_PATH" -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Ativar venv e rodar servidor (rs)"
Add-Content -Path $profilePath -Value "function rs {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "🚀 Iniciando servidor Django..." -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value "    python manage.py runserver"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Abrir shell do Django (djshell)"
Add-Content -Path $profilePath -Value "function djshell {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "🐍 Abrindo shell do Django..." -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value "    python manage.py shell"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Aplicar migrações (mig)"
Add-Content -Path $profilePath -Value "function mig {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "🔄 Aplicando migrações..." -ForegroundColor Yellow'
Add-Content -Path $profilePath -Value "    python manage.py migrate"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Criar migrações (makemig)"
Add-Content -Path $profilePath -Value "function makemig {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "📝 Criando migrações..." -ForegroundColor Yellow'
Add-Content -Path $profilePath -Value "    python manage.py makemigrations"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Ver status das migrações (showmig)"
Add-Content -Path $profilePath -Value "function showmig {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "📊 Status das migrações:" -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value "    python manage.py showmigrations"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Criar superusuário (superuser)"
Add-Content -Path $profilePath -Value "function superuser {"
Add-Content -Path $profilePath -Value "    vv"
Add-Content -Path $profilePath -Value '    Write-Host "👤 Criando superusuário..." -ForegroundColor Yellow'
Add-Content -Path $profilePath -Value "    python manage.py createsuperuser"
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Abrir API no navegador (openapi)"
Add-Content -Path $profilePath -Value "function openapi {"
Add-Content -Path $profilePath -Value '    Start-Process "http://localhost:8000/api/"'
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Abrir admin no navegador (openadmin)"
Add-Content -Path $profilePath -Value "function openadmin {"
Add-Content -Path $profilePath -Value '    Start-Process "http://localhost:8000/admin/"'
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value "# Função: Mostrar todos os aliases disponíveis (dj-help)"
Add-Content -Path $profilePath -Value "function dj-help {"
Add-Content -Path $profilePath -Value '    Write-Host ""'
Add-Content -Path $profilePath -Value '    Write-Host "🚀 Aliases Django Disponíveis:" -ForegroundColor Cyan'
Add-Content -Path $profilePath -Value '    Write-Host ""'
Add-Content -Path $profilePath -Value '    Write-Host "  vv          → Ativar ambiente virtual"'
Add-Content -Path $profilePath -Value '    Write-Host "  cdb         → Ir para diretório do backend"'
Add-Content -Path $profilePath -Value '    Write-Host "  rs          → Rodar servidor (runserver)"'
Add-Content -Path $profilePath -Value '    Write-Host "  djshell     → Abrir shell do Django"'
Add-Content -Path $profilePath -Value '    Write-Host "  mig         → Aplicar migrações (migrate)"'
Add-Content -Path $profilePath -Value '    Write-Host "  makemig     → Criar migrações (makemigrations)"'
Add-Content -Path $profilePath -Value '    Write-Host "  showmig     → Ver status das migrações"'
Add-Content -Path $profilePath -Value '    Write-Host "  superuser   → Criar superusuário"'
Add-Content -Path $profilePath -Value '    Write-Host "  openapi     → Abrir API no navegador"'
Add-Content -Path $profilePath -Value '    Write-Host "  openadmin   → Abrir admin no navegador"'
Add-Content -Path $profilePath -Value '    Write-Host "  dj-help     → Mostrar esta ajuda"'
Add-Content -Path $profilePath -Value '    Write-Host ""'
Add-Content -Path $profilePath -Value "}"
Add-Content -Path $profilePath -Value ""
Add-Content -Path $profilePath -Value 'Write-Host "✅ Aliases Django carregados! Digite dj-help para ver todos." -ForegroundColor Green'

Write-Host ""
Write-Host "✅ Aliases configurados com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Arquivo modificado: $profilePath" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Para ativar os aliases, execute um dos comandos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. Feche e abra o PowerShell novamente" -ForegroundColor White
Write-Host "   2. Ou rode: . `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "📚 Depois, digite dj-help para ver todos os atalhos!" -ForegroundColor Cyan
Write-Host ""

# Perguntar se quer recarregar agora
$reload = Read-Host "Deseja recarregar o profile agora? (S/N)"
if ($reload -eq "S" -or $reload -eq "s") {
    . $PROFILE
    Write-Host ""
    dj-help
}
