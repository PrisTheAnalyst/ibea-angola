# 🇦🇴 IBEA — Índice de Bem-Estar Económico Angola
### *Angola Economic Well-Being Index — A Real-Time Economic Intelligence System*

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento%20Activo-brightgreen)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Publicação](https://img.shields.io/badge/Publicação-Mensal-orange)](https://github.com)
[![Author](https://img.shields.io/badge/Author-PrisTheAnalyst-purple)](https://linkedin.com)

---

## 🎯 O Problema que o IBEA Resolve

Angola dispõe de dados económicos oficiais publicados com atraso de meses pelo INE e BNA.  
Esses dados capturam a economia formal — mas ignoram o que acontece nas ruas, nos mercados informais e na vida real de 34 milhões de angolanos.

**O IBEA preenche esse gap.**

É um sistema de monitorização de alta frequência que combina dados oficiais, recolha de campo e fontes abertas para produzir um índice composto mensal — o **Índice de Bem-Estar Económico Angola** — que qualquer decisor, jornalista ou investigador pode consultar, gratuitamente, em tempo real.

> *"A diferença entre dados e inteligência é o contexto. O IBEA transforma números angolanos em decisões fundamentadas."*
> — PrisTheAnalyst

---

## 📊 O Índice IBEA — Como Funciona

O IBEA é um índice composto de **0 a 100** calculado mensalmente a partir de 6 módulos independentes, cada um com peso definido pela sua elasticidade no bem-estar da população angolana.

| Módulo | Dimensão | Peso | Leading/Lagging |
|--------|----------|------|-----------------|
| M1 — Inflação Alimentar | Segurança alimentar e custo de vida | 25% | Lagging |
| M2 — Petróleo e Economia | Motor macroeconómico e receita pública | 20% | Leading |
| M3 — Salário vs Custo de Vida | Poder de compra real | 25% | Lagging |
| M4 — Kwanza e Câmbio Paralelo | Termómetro de risco e pressão inflacionária | 15% | Leading |
| M5 — Vulnerabilidade e Género | Lente ESG e desigualdade estrutural | 15% | Structural |
| **M6 — IBEA Composto** | **Consolidação matemática dos 5 módulos** | **100%** | **Composto** |

### Porquê esta ponderação?

A ponderação não é arbitrária — reflecte a **elasticidade do bem-estar no contexto angolano**:

- **M1 (25%) e M3 (25%)** dominam porque em economias em desenvolvimento, segurança alimentar e poder de compra são os principais determinantes de estabilidade social.
- **M2 (20%) e M4 (15%)** funcionam como *leading indicators* — antecipam o que acontecerá com a inflação em 30 a 60 dias, antes de os dados oficiais refletirem a realidade.
- **M5 (15%)** é o factor de ajuste ESG — garante que o índice não oculta as disparidades estruturais que os dados macro habitualmente ignoram.

---

## 🏗️ Arquitectura do Sistema

O IBEA é um **sistema de dados** com 4 camadas — não um dashboard estático.

```
┌─────────────────────────────────────────────────────────┐
│  CAMADA 1 — INGESTÃO                                    │
│  Scraping · APIs Públicas · Recolha de Campo · PDFs     │
│  BNA · INE · Banco Mundial · OPEC · Mercados Locais     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  CAMADA 2 — PROCESSAMENTO                               │
│  Python (Pandas) · SQLite/PostgreSQL                    │
│  Limpeza · Normalização · Validação · Cálculo IBEA      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  CAMADA 3 — ANÁLISE E RELATÓRIO                         │
│  Power BI · Python (Matplotlib/Plotly)                  │
│  Tendências · Alertas · Relatório PDF Mensal            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  CAMADA 4 — DISTRIBUIÇÃO PÚBLICA                        │
│  Streamlit App · GitHub · LinkedIn · PDF Report         │
│  Acesso gratuito · Publicação mensal · Open Source      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 Os 6 Módulos em Detalhe

### 🌽 M1 — Inflação Alimentar (IPA)
Monitoriza o preço de um cabaz básico de 12 produtos em Luanda e províncias.  
**Produtos:** Funge, Arroz, Óleo alimentar, Pão, Carne de frango, Peixe, Feijão, Açúcar, Tomate, Sal, Farinha de milho, Água.  
**Fontes:** Recolha de campo semanal + Kero/Jumia scraping + INE Angola.

### 🛢️ M2 — Petróleo e Economia
Correlação entre preço do Brent, produção angolana e impacto no OGE.  
**Fontes:** OPEC Monthly Report, BNA, Ministério das Finanças de Angola.

### 💵 M3 — Salário Mínimo vs Custo de Vida
Poder de compra real do salário mínimo nacional face à inflação acumulada.  
**Métrica principal:** Défice de cobertura do cabaz básico em AOA.  
**Fontes:** MAPTSS, INE Angola, dados de campo.

### 💱 M4 — Kwanza e Câmbio Paralelo
Spread entre taxa oficial BNA e mercado paralelo (Candonga). Impacto nas importações.  
**Fontes:** BNA + recolha de campo semanal + Wise API como proxy.

### 👩‍👧 M5 — Vulnerabilidade e Género
Índice de vulnerabilidade económica com lente de género e zona geográfica.  
**Fontes:** INE Angola, UNFPA Angola, dados de campo primários.

### 📊 M6 — IBEA Composto
Consolidação matemática normalizada (0–100) dos 5 módulos anteriores.  
Publicado mensalmente com relatório de variação, alertas e contexto narrativo.

---

## ⚙️ Stack Tecnológica

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| Linguagem | Python 3.10+ | Pipeline, análise, automatização |
| Processamento | Pandas, NumPy | Limpeza e transformação de dados |
| Previsão | Prophet, Scikit-learn | Modelação de tendências e sazonalidade |
| Base de Dados | PostgreSQL / SQLite | Persistência histórica dos dados |
| Automação | GitHub Actions | Pipeline CI/CD sem custo |
| Interface | Streamlit | App pública interactiva |
| Visualização | Power BI, Plotly | Dashboards e relatórios |
| Relatórios | FPDF / ReportLab | Geração automática de PDF mensal |
| Versionamento | Git + GitHub | Código aberto e histórico público |

---

## 🛡️ Resiliência de Dados — Arquitectura Fail-Safe

O sistema foi desenhado para **falhar com elegância**:

1. **Robustez de Scraping:** Se uma fonte HTML mudar, o sistema regista o erro via GitHub Actions e utiliza automaticamente a média móvel de 7 dias como valor temporário.

2. **Validação de Qualidade:** Filtro de desvio padrão — se um dado variar mais de 30% sem choque macroeconómico correspondente, é marcado para revisão manual (*Human-in-the-loop*).

3. **Fontes Alternativas:** Se os dados oficiais do INE atrasarem, o M4 usa proxies de mercado (Wise/spread bancário) para estimar a pressão inflacionária.

---

## 🗓️ Roadmap de Implementação

```
Semana 1-2  ▓▓░░░░░░  Fundação: dados, metodologia, estrutura GitHub
Semana 3-4  ░░▓▓░░░░  Pipeline Python v1 + SQLite + IPA funcional
Semana 5-6  ░░░░▓▓░░  Módulos M2-M5 + Streamlit app online
Semana 7-8  ░░░░░░▓▓  IBEA composto + Power BI + 1ª publicação pública
```

**Fase actual:** Semana 1 — Fundação e estrutura do sistema.  
**Próxima milestone:** Pipeline de ingestão do M1 funcional.  
**Primeira publicação pública:** Prevista para [mês/ano].

---

## 📁 Estrutura do Repositório

```
ibea-angola/
│
├── README.md                    # Este ficheiro
├── LICENSE                      # MIT License
├── requirements.txt             # Dependências Python
├── .gitignore                   # Ficheiros ignorados
│
├── data/
│   ├── raw/                     # Dados brutos por fonte
│   │   ├── campo/               # Recolhas manuais (Excel/CSV)
│   │   ├── bna/                 # Dados Banco Nacional de Angola
│   │   ├── ine/                 # Dados INE Angola
│   │   └── opec/                # Dados OPEC/petróleo
│   ├── processed/               # Dados limpos e normalizados
│   └── historical/              # Séries históricas mensais
│
├── pipeline/
│   ├── ingestion/               # Scripts de recolha de dados
│   │   ├── scraper_precos.py    # Scraping de preços alimentares
│   │   ├── api_bna.py           # Ingestão dados BNA
│   │   └── loader_campo.py      # Carregamento de dados de campo
│   ├── processing/              # Limpeza e transformação
│   │   ├── cleaner.py           # Limpeza e validação
│   │   ├── normalizer.py        # Normalização 0-100
│   │   └── calculator_ibea.py   # Cálculo do índice composto
│   └── automation/              # GitHub Actions
│       └── monthly_run.yml      # Pipeline mensal automatizado
│
├── notebooks/
│   ├── 01_exploratory_m1.ipynb  # Análise exploratória M1
│   ├── 02_exploratory_m2.ipynb  # Análise exploratória M2
│   ├── 03_ibea_methodology.ipynb# Metodologia e validação IBEA
│   └── 04_forecasting.ipynb     # Modelos de previsão
│
├── app/
│   ├── main.py                  # App Streamlit principal
│   ├── pages/                   # Páginas por módulo
│   │   ├── m1_inflacao.py
│   │   ├── m2_petroleo.py
│   │   ├── m3_salario.py
│   │   ├── m4_cambio.py
│   │   ├── m5_genero.py
│   │   └── m6_ibea.py
│   └── components/              # Componentes reutilizáveis
│
├── reports/
│   ├── template/                # Template PDF do relatório mensal
│   ├── 2025/                    # Relatórios publicados por ano
│   └── generator.py             # Script de geração automática PDF
│
└── docs/
    ├── metodologia.md           # Documentação técnica da metodologia
    ├── fontes.md                # Fontes de dados e credibilidade
    ├── glossario.md             # Glossário de termos económicos
    └── architecture.png         # Diagrama de arquitectura
```

---

## 🌍 Impacto e Público-Alvo

| Público | Como usa o IBEA |
|---------|----------------|
| Decisores políticos | Monitorização mensal do bem-estar económico |
| Investidores internacionais | Due diligence e análise de risco Angola |
| ONGs e organismos internacionais | Dados de vulnerabilidade e género |
| Jornalistas e investigadores | Fonte aberta para reportagem económica |
| PMEs angolanas | Contexto de mercado para decisões de negócio |

---

## 👤 Sobre o Projecto

**Autora:** PrisTheAnalyst  
**Contexto:** Projecto de dados independente, open-source, sem fins comerciais.  
**Motivação:** Preencher o gap de inteligência económica em tempo real sobre Angola — combinando rigor técnico com conhecimento profundo do contexto local.

> *"Não construo dashboards. Construo sistemas que transformam a realidade angolana em dados que o mundo consegue ler."*

📧 [Contacto via LinkedIn]  
🔗 [App Streamlit — em breve]  
📄 [Primeiro relatório IBEA — em breve]

---

## 📜 Licença

MIT License — livre para usar, adaptar e distribuir com atribuição.

---

*Última actualização: Maio 2025 · Fase: Implementação Activa · Próxima publicação: a definir*
