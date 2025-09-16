# Introdução

## Visão Geral do Projeto

Este projeto foi desenvolvido como parte da disciplina **REQ-T1** do curso de Engenharia de Software, período 2025.2, em parceria com a **Softex** (Associação para Promoção da Excelência do Software Brasileiro).

## Objetivo Principal

Desenvolver um **sistema centralizado de gestão de recursos físicos** (salas de reunião e estações de trabalho) para a Softex, eliminando o processo manual e fragmentado atual que gera conflitos de reserva, retrabalho administrativo e baixa visibilidade da ocupação.

## Contexto do Negócio

A Softex é uma entidade sem fins lucrativos dedicada ao fortalecimento do setor de tecnologia e software no Brasil, com mais de 25 anos de atuação. A instituição opera em modelo de trabalho híbrido, exigindo coordenação eficiente de recursos físicos de escritório.

### Problema Identificado

A Softex não possui um processo/sistema centralizado para gerir o uso dos recursos físicos do escritório. O fluxo atual, manual e fragmentado (planilhas, calendários e trocas por mensagem), gera:

- Conflitos de reserva
- Retrabalho administrativo  
- Baixa visibilidade da ocupação
- Dificuldade no planejamento do espaço no modelo híbrido

## Solução Proposta

Um sistema web que oferece:

- **Reserva de Salas**: Reservas online simples e rápidas com prevenção automática de conflitos
- **Mapa Interativo**: Visualização em tempo real de salas disponíveis/ocupadas
- **Gestão de Capacidade**: Controle de regras de uso conforme políticas internas
- **Relatórios e Indicadores**: Métricas de utilização para apoio à gestão
- **Integração Corporativa**: Sincronização com Google Calendar e notificações via Slack

## Tecnologias Utilizadas

### Frontend
- **Vue.js**: Framework moderno e reativo para interface do usuário

### Backend  
- **Python + Django REST Framework**: API robusta e escalável
- **PostgreSQL**: Banco de dados relacional confiável

### Infraestrutura
- **Docker**: Containerização para deploy padronizado
- **GitHub**: Controle de versão e colaboração
- **AWS**: Hospedagem em nuvem

### Integrações
- **Google Calendar**: Sincronização de reservas
- **Slack**: Notificações automáticas
- **Google Workspace SSO**: Autenticação integrada

## Metodologia de Desenvolvimento

- **Processo**: Agile Unified Process (AUP)
- **Ciclo de Vida**: Iterativo/Incremental
- **Duração**: 12 semanas (14/09/2025 a 09/12/2025)
- **Entregas**: Quinzenais com validação do cliente

## Estrutura da Documentação

Esta documentação está organizada nas seguintes seções:

- **Cenário Atual**: Contexto do cliente e identificação do problema
- **Solução Proposta**: Características e tecnologias da solução
- **Estratégias de Engenharia**: Metodologia e processo de desenvolvimento
- **Cronograma**: Planejamento e entregas do projeto
- **Interação Equipe-Cliente**: Comunicação e validação
- **Lições Aprendidas**: Reflexões e melhorias do processo

## Equipe do Projeto

<div class="team-grid">
  <div class="team-card">
    <img src="https://github.com/gusmoles.png" alt="Guilherme Gusmão" class="team-photo">
    <div class="team-info">
      <h3>Guilherme Gusmão</h3>
      <p class="team-role">Frontend (Vue.js)</p>
      <p class="team-github">@gusmoles</p>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/darkymeubem.png" alt="Felipe Pedroza" class="team-photo">
    <div class="team-info">
      <h3>Felipe Pedroza</h3>
      <p class="team-role">Backend (Python/DRF) & Análise de Requisitos</p>
      <p class="team-github">@darkymeubem</p>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/camposs04.png" alt="Júlia Santana" class="team-photo">
    <div class="team-info">
      <h3>Júlia Santana</h3>
      <p class="team-role">Modelagem de Dados</p>
      <p class="team-github">@camposs04</p>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/Pietrocv.png" alt="Pietro Calegari" class="team-photo">
    <div class="team-info">
      <h3>Pietro Calegari</h3>
      <p class="team-role">Backend (Python/DRF)</p>
      <p class="team-github">@Pietrocv</p>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/rich4rd1.png" alt="Kauã Richard" class="team-photo">
    <div class="team-info">
      <h3>Kauã Richard</h3>
      <p class="team-role">DevOps/Infraestrutura & Qualidade (QA)</p>
      <p class="team-github">@rich4rd1</p>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/y123yuri.png" alt="Yuri Andrade" class="team-photo">
    <div class="team-info">
      <h3>Yuri Andrade</h3>
      <p class="team-role">Gerência do Projeto & DevOps</p>
      <p class="team-github">@y123yuri</p>
    </div>
  </div>
</div>
