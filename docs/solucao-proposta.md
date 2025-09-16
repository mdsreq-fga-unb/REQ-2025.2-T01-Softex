# Solução Proposta

## 2.1 Objetivo do Produto

O principal objetivo do produto é eliminar as ineficiências do processo atual, que é manual e suscetível a conflitos, garantindo maior fluidez na organização do espaço físico e no modelo de trabalho híbrido. Também gerar relatórios que façam sentido para a organização.

### Resultados Esperados

#### Otimização da Utilização do Espaço
Permitir que colaboradores planejem com antecedência sua presença no escritório, garantindo previsibilidade e reduzindo conflitos no uso de salas e estações.

#### Aumento da Produtividade Interna
Reduzir o tempo gasto em tarefas administrativas e na resolução de conflitos de reserva, liberando os colaboradores para focarem em suas atividades principais.

#### Autonomia e Conveniência para os Colaboradores
Estabelecer um processo centralizado e acessível de agendamento de recursos, sem necessidade de intermediários.

#### Visibilidade Estratégica para a Gestão
Disponibilizar dados consistentes sobre taxa de ocupação e padrões de uso do escritório, possibilitando decisões mais embasadas sobre infraestrutura e custos operacionais.

#### Apoio à Adesão ao Modelo Híbrido
Tornar a experiência do trabalho presencial mais organizada e eficiente, fortalecendo a integração entre equipes e a colaboração no ambiente físico.

## 2.2 Características da Solução

A solução proposta terá como foco apoiar a organização e o planejamento do modelo híbrido da empresa, garantindo o uso eficiente das salas e ambientes de trabalho.

### Funcionalidades Principais

#### Reserva de Salas
- Reservas online simples e rápidas
- Prevenção automática de conflitos
- Melhor controle de uso dos espaços

#### Mapa Interativo de Ocupação
- Visualização em tempo real de salas disponíveis/ocupadas
- Apoio à decisão imediata

#### Gestão de Capacidade e Regras de Uso
- Limites por sala conforme políticas internas e normas de segurança
- Uso dentro da capacidade adequada

#### Relatórios e Indicadores de Utilização
- Métricas de frequência de uso
- Horários de pico e uso por equipe
- Apoio a reorganização ou expansão da infraestrutura

#### Controle de Permissões e Perfis de Acesso
- Perfis por cargo/setor/equipe
- Possibilidade de bloqueio ou prioridade de uso em situações específicas

#### Integração com Ferramentas Corporativas
- Sincronização com calendários (Google Workspace) para evitar conflitos
- Notificações automáticas de confirmação e lembrete (ex.: Slack)

#### Flexibilidade para Diferentes Ambientes
- Funcionamento para coworking interno, salas de reunião, hubs de inovação e escritórios satélites
- Escalável para múltiplas unidades da empresa

## 2.3 Tecnologias a Serem Utilizadas

### Frontend
**Vue.js** - Escolhido por sua facilidade de uso, curva de aprendizado rápida e pela preferência da empresa em adotar uma interface moderna e simples de manter.

### Backend
**Python com Django REST Framework (DRF)** - A escolha se justifica pelo uso já consolidado da linguagem dentro da Softex, além da facilidade na geração de relatórios e da ampla oferta de bibliotecas para manipulação e análise de dados, características que fortalecem a aderência e a eficiência do projeto.

### Banco de Dados
**PostgreSQL** - Solução amplamente utilizada e já consolidada na infraestrutura da empresa, garantindo confiabilidade, robustez e recursos avançados para consultas e relatórios.

### Controle de Versão
**Git com GitHub** - Para versionamento de código, utilizando também Issues e Projects para organização de tarefas e acompanhamento do desenvolvimento.

### Containerização
**Docker** - Para empacotamento e implantação do sistema. Essa escolha facilita a criação de ambientes padronizados, reduz problemas de compatibilidade e garante agilidade no processo de deploy. A empresa já possui experiência com Docker, o que favorece a integração do novo sistema à sua infraestrutura existente.

### Integrações Corporativas
- **Google Calendar**: Para sincronização de reservas (bloqueios, atualizações e cancelamentos)
- **Slack**: Para envio de confirmações e lembretes de agendamento
- **SSO via Google Workspace**: Para autenticação segura e integrada ao ambiente organizacional

## 2.4 Pesquisa de Mercado e Análise Competitiva

### Análise dos Concorrentes

#### Skedda
- **Problemas**: Relatórios pouco úteis; integrações limitadas; interface considerada datada em alguns relatos

#### Envoy Workplace/Desks
- **Problemas**: Edição de reservas incômoda; limitações em certos fluxos

#### Robin
- **Problemas**: Custo alto e add-ons caros; notificações inconsistentes; lentidão em ambientes grandes

#### OfficeSpace
- **Problemas**: Atualização não imediata sem refresh; recursos faltando em comparação a concorrentes

#### Eptura (Condeco/Engage)
- **Problemas**: Integrações instáveis com suites de colaboração; funcionalidades limitadas; suporte percebido como fraco em alguns casos

#### WorkInSync
- **Problemas**: App lento/travando em pico; necessidade de relatórios mais robustos

### Problemas Transversais Identificados
- Integrações incompletas com calendários/colaboração
- Analytics rasos ou presos a planos superiores
- UX fraca para editar/cancelar (ex.: sem autosave)
- Custo/precificação com funcionalidades relevantes em tiers altos

## 2.5 Viabilidade da Solução

### Viabilidade Técnica
Tecnologias definidas (Vue.js, Python/DRF, PostgreSQL, Docker em AWS) são maduras e bem documentadas; Python facilita integrações e geração de relatórios; arquitetura por APIs permite evolução.

**Riscos**: Mapa interativo (UI/UX + tempo de backend), permissões granulares (modelagem/segurança), responsividade/PWA (testes multiplataforma).

**Conclusão**: Viável com time full-stack e integração de APIs.

### Viabilidade de Prazo
Meta de MVP até início de novembro com escopo claro e sprints quinzenais. Risco principal: mapa interativo e permissões podem alongar cronograma se não priorizados desde o início.

**Conclusão**: Viável com planejamento de sprints e foco no essencial do MVP.

### Viabilidade Financeira
Evita contratação de ferramenta externa (economia estimada R$ 10–20 mil/ano); uso de AWS já disponível reduz custo inicial; projeto universitário reduz custo de desenvolvimento.

**Custos potenciais**: Horas de desenvolvimento, manutenção evolutiva e variação de custo AWS conforme uso.

**Conclusão**: Alto custo-benefício.

### Viabilidade de Mercado
Necessidade já comprovada internamente (58 posições de coworking e 6 salas); solução aderente às políticas da organização e replicável em outras unidades.

**Conclusão**: Alinhada à demanda, com potencial de expansão.

### Sustentabilidade
Stack amplamente suportada, código sob domínio da Softex, implantação padronizada via Docker e escala em nuvem (AWS).

**Conclusão**: Sustentável e escalável no longo prazo.

### Conclusão Geral
A ferramenta de gestão de coworking e salas de reunião é tecnicamente viável, financeiramente vantajosa, executável dentro do prazo e atende à demanda real da Softex. O maior desafio será garantir o desenvolvimento do mapa interativo e do sistema de permissões dentro do cronograma, mas, com uma abordagem ágil e priorização correta, o projeto tem alto potencial de sucesso e retorno sobre investimento positivo.

## 2.6 Impacto da Solução

### Impacto Operacional
A centralização e a padronização do processo reduzem o tempo de agendamento, evitam conflitos e diminuem retrabalho administrativo. Na prática, o fluxo deixa de depender de trocas manuais e passa a acontecer em poucos passos, com confirmação imediata e prevenção de duplicidades.

### Experiência do Colaborador
Com disponibilidade em tempo real e autoatendimento, a ida ao escritório fica previsível e sem "negociação" por mensagens ou planilhas. Equipes conseguem organizar a semana presencial em minutos, com menos interrupções e maior foco.

### Visibilidade Gerencial e Uso do Espaço
Relatórios confiáveis de ocupação e no-show revelam padrões (picos, ociosidade, salas mais demandadas) e orientam ajustes de política e layout. Isso melhora o aproveitamento do ambiente sem necessidade imediata de ampliar infraestrutura.

### Governança e Conformidade
Regras claras (capacidade, janelas, limites, no-show) passam a ser aplicadas de forma uniforme, com trilha de auditoria de reservas e alterações. Reduz-se a subjetividade em disputas e ganha-se segurança para revisões internas.

### Integração ao Ecossistema Corporativo
Sincronização com Google Calendar e avisos no Slack consolidam o processo oficial e evitam comunicações dispersas. SSO simplifica a gestão de acesso e aumenta a aderência às políticas internas.

### Produtividade e Custo-Benefício
A automatização libera tempo de administradores e usuários, melhora o retorno de esforço do time e evita gastos recorrentes com ferramentas externas. O ganho se amplia conforme aumentam as reservas e a adesão ao processo centralizado.

### Escalabilidade e Sustentabilidade
Arquitetura por APIs e uso de Docker facilitam replicação para outras unidades, padronizam deploy e manutenção e abrem caminho para evolução contínua (novos painéis, políticas dinâmicas, integrações).
