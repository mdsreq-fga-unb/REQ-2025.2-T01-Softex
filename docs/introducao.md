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

## Equipe do Projeto

- **Gerência do Projeto**: Yuri
- **Frontend (Vue.js)**: Guilherme (Gusmão)
- **Backend (Python/DRF)**: Felipe e Pietro
- **DevOps/Infraestrutura**: Yuri e Kauã
- **Modelagem de Dados**: Júlia
- **Análise de Requisitos**: Felipe
- **Qualidade (QA)**: Kauã

## Estrutura da Documentação

Esta documentação está organizada nas seguintes seções:

- **Cenário Atual**: Contexto do cliente e identificação do problema
- **Solução Proposta**: Características e tecnologias da solução
- **Estratégias de Engenharia**: Metodologia e processo de desenvolvimento
- **Cronograma**: Planejamento e entregas do projeto
- **Interação Equipe-Cliente**: Comunicação e validação
- **Lições Aprendidas**: Reflexões e melhorias do processo
