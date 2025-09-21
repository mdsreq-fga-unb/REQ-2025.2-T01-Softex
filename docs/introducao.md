# Introdução

## Visão Geral do Projeto

Projeto da disciplina **REQ-T1** (Engenharia de Software - 2025.2) em parceria com a **Softex** para desenvolvimento de um sistema centralizado de gestão de recursos físicos.

## Objetivo Principal

Desenvolver um **sistema centralizado de gestão de recursos físicos** (salas de reunião e estações de trabalho) para a Softex, eliminando o processo manual e fragmentado atual.

## Contexto do Negócio

A Softex é uma entidade sem fins lucrativos com mais de 25 anos de atuação no setor de tecnologia brasileiro, operando em modelo de trabalho híbrido que exige coordenação eficiente de recursos físicos.

### Problema Identificado

A Softex não possui um processo/sistema centralizado para gerir recursos físicos. O fluxo atual, manual e fragmentado, gera conflitos de reserva, retrabalho administrativo e baixa visibilidade da ocupação.

## Solução Proposta

Sistema web com reservas online, mapa interativo de ocupação, gestão de capacidade, relatórios e integração corporativa (Google Calendar + Slack).

### Arquitetura do Sistema

```mermaid
graph TB
    A[Usuário] --> B[Frontend Vue.js]
    B --> C[API Django REST]
    C --> D[PostgreSQL]
    C --> E[Google Calendar API]
    C --> F[Slack API]
    B --> G[Docker Container]
    G --> H[AWS Cloud]
    
    subgraph "Integrações"
        E
        F
    end
    
    subgraph "Infraestrutura"
        G
        H
    end
```

## Tecnologias Utilizadas

| Categoria | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Frontend** | Vue.js | Framework moderno e reativo para interface do usuário |
| **Backend** | Python + Django REST Framework | API robusta e escalável |
| **Backend** | PostgreSQL | Banco de dados relacional confiável |
| **Infraestrutura** | Docker | Containerização para deploy padronizado |
| **Infraestrutura** | GitHub | Controle de versão e colaboração |
| **Infraestrutura** | AWS | Hospedagem em nuvem |
| **Integrações** | Google Calendar | Sincronização de reservas |
| **Integrações** | Slack | Notificações automáticas |
| **Integrações** | Google Workspace SSO | Autenticação integrada |

## Metodologia de Desenvolvimento

| Aspecto | Detalhes |
|---------|----------|
| **Processo** | Agile Unified Process (AUP) |
| **Ciclo de Vida** | Iterativo/Incremental |
| **Duração** | 12 semanas (14/09/2025 a 09/12/2025) |
| **Entregas** | Quinzenais com validação do cliente |

## Estrutura da Documentação

| Seção | Descrição |
|-------|-----------|
| **Cenário Atual** | Contexto do cliente e identificação do problema |
| **Solução Proposta** | Características e tecnologias da solução |
| **Estratégias de Engenharia** | Metodologia e processo de desenvolvimento |
| **Cronograma** | Planejamento e entregas do projeto |
| **Interação Equipe-Cliente** | Comunicação e validação |
| **Lições Aprendidas** | Reflexões e melhorias do processo |

## Equipe do Projeto

<div class="team-grid">
  <div class="team-card">
    <img src="https://github.com/y123yuri.png" alt="Yuri Andrade" class="team-photo">
    <div class="team-info">
      <h3>Yuri Andrade</h3>
      <p class="team-role">Gerência do Projeto & DevOps</p>
      <a href="https://github.com/y123yuri" class="team-github">@y123yuri</a>
    </div>
  </div>
  <div class="team-card">
    <img src="https://github.com/gusmoles.png" alt="Guilherme Gusmão" class="team-photo">
    <div class="team-info">
      <h3>Guilherme Gusmão</h3>
      <p class="team-role">Frontend (Vue.js)</p>
      <a href="https://github.com/gusmoles" class="team-github">@gusmoles</a>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/darkymeubem.png" alt="Felipe Pedroza" class="team-photo">
    <div class="team-info">
      <h3>Felipe Pedroza</h3>
      <p class="team-role">Backend (Python/DRF) & Análise de Requisitos</p>
      <a href="https://github.com/darkymeubem" class="team-github">@darkymeubem</a>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/camposs04.png" alt="Júlia Santana" class="team-photo">
    <div class="team-info">
      <h3>Júlia Santana</h3>
      <p class="team-role">Modelagem de Dados</p>
      <a href="https://github.com/camposs04" class="team-github">@camposs04</a>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/Pietrocv.png" alt="Pietro Calegari" class="team-photo">
    <div class="team-info">
      <h3>Pietro Calegari</h3>
      <p class="team-role">Backend (Python/DRF)</p>
      <a href="https://github.com/Pietrocv" class="team-github">@Pietrocv</a>
    </div>
  </div>

  <div class="team-card">
    <img src="https://github.com/rich4rd1.png" alt="Kauã Richard" class="team-photo">
    <div class="team-info">
      <h3>Kauã Richard</h3>
      <p class="team-role">DevOps/Infraestrutura & Qualidade (QA)</p>
      <a href="https://github.com/rich4rd1" class="team-github">@rich4rd1</a>
    </div>
  </div>

</div>
