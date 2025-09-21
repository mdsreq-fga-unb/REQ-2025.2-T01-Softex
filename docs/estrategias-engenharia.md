# Estratégias de Engenharia de Software

## 3.1 Estratégia Priorizada

### Abordagem de Desenvolvimento de Software
**Híbrida** (combina práticas preditivas e ágeis, conciliando disciplina com flexibilidade).

### Ciclo de Vida
**Iterativo/Incremental**

### Processo de Engenharia de Software
**Agile Unified Process (AUP)**

## 3.2 Quadro Comparativo

| Aspecto | **AUP** | **RAD** |
|---------|---------|---------|
| **Características** | Combina princípios ágeis com RUP | Desenvolvimento acelerado baseado em prototipação |
| **Ciclo** | Iterativo/incremental com documentação enxuta | Iterativo com foco em entregas funcionais rápidas |
| **Fases** | Modelagem, Implementação, Teste, Implantação | Prototipação contínua com feedback do usuário |
| **Vantagens** | • Evolução contínua do sistema<br>• Mais leve que RUP<br>• Disciplina técnica | • Redução significativa do tempo<br>• Excelente para validação<br>• Alta interação com cliente |
| **Desvantagens** | Menos prescritivo (inconsistência em equipes inexperientes) | • Arquitetura fraca se mal planejado<br>• Pouco adequado para sistemas críticos |
| **Quando usar** | Projetos de médio porte com agilidade + qualidade | Startups, protótipos, validação frequente |

## 3.3 Justificativa

O **AUP** foi escolhido em detrimento do RAD considerando as características do produto, da equipe e do prazo disponível.

### Por que o AUP é mais adequado

| Aspecto | Justificativa |
|---------|---------------|
| **Equilíbrio Agilidade/Disciplina** | Entregas incrementais com fases bem definidas (modelagem, implementação, testes, implantação) |
| **Escopo do Projeto** | Suporte a funcionalidades críticas (reservas em tempo real, permissões, integrações) |
| **Equipe Acadêmica** | Favorece divisão de tarefas em ciclos curtos com aprendizado de boas práticas |

### Por que o RAD não seria adequado

| Problema | Impacto |
|----------|---------|
| **Foco excessivo em prototipação** | Protótipos podem não evoluir para arquitetura sólida |
| **Menor preocupação com engenharia** | Pode deixar de lado modelagem, testes e documentação |
| **Instabilidade em equipes acadêmicas** | Exige cliente muito ativo e equipes maduras |
| **Inadequado para sistemas críticos** | Rapidez pode comprometer confiabilidade |

### Conclusão
O AUP permite entregas ágeis e incrementais sem abrir mão da disciplina técnica necessária para um sistema confiável e escalável.

## 3.4 Estrutura do Processo AUP

### Fases Principais

| Fase | Atividades |
|------|------------|
| **1. Modelagem** | • Levantamento e análise de requisitos<br>• Design da arquitetura do sistema<br>• Criação de diagramas e documentação técnica |
| **2. Implementação** | • Desenvolvimento das funcionalidades<br>• Programação seguindo padrões estabelecidos<br>• Integração entre componentes |
| **3. Teste** | • Testes unitários e de integração<br>• Testes de aceitação com o cliente<br>• Validação de funcionalidades |
| **4. Implantação** | • Deploy em ambiente de produção<br>• Treinamento dos usuários<br>• Monitoramento e ajustes |

### Características do AUP Aplicadas ao Projeto

| Característica | Implementação |
|----------------|---------------|
| **Iterações Curtas** | Sprints de 2 semanas com entregas incrementais funcionais |
| **Documentação Enxuta** | Foco na documentação essencial e código auto-documentado |
| **Disciplina Técnica** | Padrões de codificação, testes automatizados e controle de qualidade |
| **Adaptabilidade** | Ajustes baseados no feedback e priorização dinâmica |
