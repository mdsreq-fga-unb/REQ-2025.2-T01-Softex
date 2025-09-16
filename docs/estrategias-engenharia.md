# Estratégias de Engenharia de Software

## 3.1 Estratégia Priorizada

### Abordagem de Desenvolvimento de Software
**Híbrida** (combina práticas preditivas e ágeis, conciliando disciplina com flexibilidade).

### Ciclo de Vida
**Iterativo/Incremental**

### Processo de Engenharia de Software
**Agile Unified Process (AUP)**

## 3.2 Quadro Comparativo

### Agile Unified Process (AUP)

#### Características
- Combina princípios ágeis com o Rational Unified Process (RUP)
- Utiliza um ciclo iterativo e incremental, mas com documentação mais enxuta
- Estruturado em fases principais: Modelagem, Implementação, Teste e Implantação

#### Vantagens
- Iterativo e incremental, favorecendo evolução contínua do sistema
- Mais leve que o RUP, adequado para entregas rápidas
- Mantém práticas de engenharia de software disciplinadas

#### Desvantagens
- Menos prescritivo → pode gerar inconsistência em equipes pouco experientes

#### Quando usar
- Projetos de médio porte que necessitam de entregas rápidas e disciplina técnica
- Projetos em que agilidade e qualidade técnica precisam coexistir

### Rapid Application Development (RAD)

#### Características
- Desenvolvimento acelerado baseado em prototipação
- Iterativo, com foco em entregas funcionais rápidas
- Envolve feedback constante do usuário

#### Vantagens
- Reduz significativamente o tempo de desenvolvimento
- Excelente para validação de requisitos via protótipos
- Promove alta interação com o cliente

#### Desvantagens
- Pode gerar arquitetura fraca se os protótipos não forem bem planejados
- Pouco adequado para sistemas críticos

#### Quando usar
- Projetos que exigem entregas rápidas e validação frequente dos requisitos
- Startups, protótipos de sistemas ou aplicações comerciais de mercado

## 3.3 Justificativa

O processo escolhido para o desenvolvimento do projeto é o **Agile Unified Process (AUP)**, em detrimento do Rapid Application Development (RAD), considerando as características do produto, da equipe e do prazo disponível.

### Por que o AUP é mais adequado

#### Equilíbrio entre Agilidade e Disciplina Técnica
O AUP permite entregas incrementais a cada sprint, mas preserva fases bem definidas de modelagem, implementação, testes e implantação. Isso garante que o sistema evolua de forma estruturada, sem comprometer a qualidade ou a arquitetura.

#### Escopo do Projeto
O sistema de gerenciamento de co-working exige funcionalidades críticas, como:
- Reservas em tempo real
- Controle de permissões por papéis (líder, chefe, subordinado)
- Integração de diferentes fluxos de uso

O AUP oferece suporte a esse nível de complexidade, ao mesmo tempo em que mantém a possibilidade de adaptação ao longo do desenvolvimento.

#### Equipe Acadêmica
Como o projeto é desenvolvido em um contexto de faculdade, por uma equipe de 6 integrantes, o AUP favorece a divisão de tarefas em ciclos curtos, permitindo aprendizado de boas práticas de engenharia de software sem abrir mão de produtividade.

### Por que o RAD não seria tão adequado

#### Foco Excessivo em Prototipação
O RAD é excelente para validar rapidamente requisitos com o cliente, mas tende a gerar protótipos que nem sempre evoluem para uma arquitetura sólida. Para um sistema de médio porte, que precisa ser mantido até o final do semestre e apresentar consistência técnica, essa fragilidade pode ser um risco.

#### Menor Preocupação com Engenharia de Software
Por priorizar velocidade e interação intensa com o cliente, o RAD pode deixar de lado práticas como:
- Modelagem adequada
- Testes bem estruturados
- Documentação mínima necessária

Isso pode resultar em retrabalho, especialmente em um sistema com diferentes tipos de usuários e regras de negócio específicas.

#### Possível Instabilidade em Equipes Acadêmicas
O RAD exige um cliente extremamente ativo no processo e equipes maduras em desenvolvimento rápido. No contexto acadêmico, onde ainda se está aprendendo a organizar sprints, dividir papéis e controlar qualidade, essa abordagem poderia gerar mais confusão do que resultados consistentes.

#### Menos Adequado para Sistemas com Regras Críticas
No caso de um sistema de reservas em tempo real, falhas ou inconsistências podem prejudicar toda a lógica de funcionamento. O RAD, por privilegiar rapidez de entrega, poderia comprometer a confiabilidade dessas funcionalidades.

### Conclusão

Dessa forma, o AUP é mais indicado para o projeto, pois possibilita entregas ágeis e incrementais alinhadas ao cronograma de sprints, mas sem abrir mão da disciplina técnica necessária para construir um sistema confiável, escalável e coerente. 

O RAD, embora vantajoso em contextos de prototipação rápida ou startups que precisam apenas validar ideias iniciais, não seria tão eficaz para um sistema acadêmico que exige consistência arquitetural, controle de usuários e funcionalidades críticas de gerenciamento.

## 3.4 Estrutura do Processo AUP

### Fases Principais

#### 1. Modelagem
- Levantamento e análise de requisitos
- Design da arquitetura do sistema
- Criação de diagramas e documentação técnica

#### 2. Implementação
- Desenvolvimento das funcionalidades
- Programação seguindo padrões estabelecidos
- Integração entre componentes

#### 3. Teste
- Testes unitários e de integração
- Testes de aceitação com o cliente
- Validação de funcionalidades

#### 4. Implantação
- Deploy em ambiente de produção
- Treinamento dos usuários
- Monitoramento e ajustes

### Características do AUP Aplicadas ao Projeto

#### Iterações Curtas
- Sprints de 2 semanas
- Entregas incrementais funcionais
- Feedback contínuo do cliente

#### Documentação Enxuta
- Foco na documentação essencial
- Diagramas quando necessário
- Código auto-documentado

#### Disciplina Técnica
- Padrões de codificação
- Testes automatizados
- Controle de qualidade

#### Adaptabilidade
- Ajustes baseados no feedback
- Priorização dinâmica
- Resposta rápida a mudanças
