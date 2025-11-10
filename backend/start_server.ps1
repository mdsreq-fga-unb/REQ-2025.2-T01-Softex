# ========================================
# Script para Iniciar o Servidor Django
# ========================================
# Uso: .\start_server.ps1

Write-Host "🚀 Iniciando Backend Softex..." -ForegroundColor Cyan
Write-Host ""

# Verificar se está no diretório correto
if (-Not (Test-Path "manage.py")) {
    Write-Host "❌ Erro: Não encontrei o arquivo manage.py!" -ForegroundColor Red
    Write-Host "Execute este script dentro do diretório backend/" -ForegroundColor Yellow
    exit 1
}

# Ativar ambiente virtual
Write-Host "📦 Ativando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Ambiente virtual ativado!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Crie com: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🔍 Verificando banco de dados..." -ForegroundColor Yellow

# Verificar se há migrações pendentes
$migrations = python manage.py showmigrations --plan 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Problema ao conectar com o banco!" -ForegroundColor Red
    Write-Host "Verifique as configurações no arquivo .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Banco de dados OK!" -ForegroundColor Green
Write-Host ""

# Iniciar servidor
Write-Host "🌐 Iniciando servidor Django..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  Servidor rodando em:" -ForegroundColor Green
Write-Host "  http://localhost:8000/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Green
Write-Host "  API disponível em:" -ForegroundColor Green
Write-Host "  http://localhost:8000/api/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Green
Write-Host "  Admin disponível em:" -ForegroundColor Green
Write-Host "  http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

