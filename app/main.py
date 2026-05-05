"""
IBEA — Interface pública Streamlit
Ponto 4: Dashboard com dados simulados reais
Autora: PrisTheAnalyst
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="IBEA — Angola Economic Monitor",
    page_icon="🇦🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DADOS SIMULADOS (substituir por CSV real depois)
# ─────────────────────────────────────────────

@st.cache_data
def carregar_dados():
    np.random.seed(42)
    meses = pd.date_range(start="2023-01-01", periods=18, freq="MS")

    df = pd.DataFrame({
        "mes":         meses,
        "m1_inflacao": np.round(65 + np.cumsum(np.random.uniform(-2, -0.2, 18)), 1).clip(0, 100),
        "m2_petroleo": np.round(55 + np.cumsum(np.random.uniform(-3,  0.5, 18)), 1).clip(0, 100),
        "m3_salario":  np.round(50 + np.cumsum(np.random.uniform(-2, -0.3, 18)), 1).clip(0, 100),
        "m4_cambio":   np.round(48 + np.cumsum(np.random.uniform(-2.5, 0.2, 18)), 1).clip(0, 100),
        "m5_genero":   np.round(42 + np.cumsum(np.random.uniform(-1,   0.1, 18)), 1).clip(0, 100),
    })

    df["ibea_score"] = (
        df["m1_inflacao"] * 0.25 +
        df["m2_petroleo"] * 0.20 +
        df["m3_salario"]  * 0.25 +
        df["m4_cambio"]   * 0.15 +
        df["m5_genero"]   * 0.15
    ).round(2)

    df["cabaz_aoa"] = np.round(
        12000 + np.cumsum(np.random.uniform(200, 600, 18)), 0
    )
    df["salario_minimo_aoa"] = [
        32000, 32000, 32000, 32000, 32000, 32000,
        36000, 36000, 36000, 36000, 36000, 36000,
        40000, 40000, 40000, 40000, 40000, 40000
    ]
    df["poder_compra_pct"] = (df["salario_minimo_aoa"] / df["cabaz_aoa"] * 100).round(1)

    return df


def classificar(score):
    if score >= 75:   return "🟢 Bem-estar Elevado",   "#27AE60"
    elif score >= 55: return "🟡 Bem-estar Moderado",  "#F1C40F"
    elif score >= 35: return "🟠 Bem-estar Baixo",     "#E67E22"
    elif score >= 20: return "🔴 Bem-estar Crítico",   "#E74C3C"
    else:             return "⚫ Situação de Colapso", "#2C3E50"


df = carregar_dados()
ultimo = df.iloc[-1]
penultimo = df.iloc[-2]
classificacao, cor_ibea = classificar(ultimo["ibea_score"])

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.image("https://flagcdn.com/w80/ao.png", width=50)
st.sidebar.title("IBEA")
st.sidebar.caption("Índice de Bem-Estar Económico Angola")
st.sidebar.markdown("---")

pagina = st.sidebar.radio("Navegar:", [
    "🏠 Visão Geral",
    "🌽 M1 — Inflação Alimentar",
    "🛢️ M2 — Petróleo",
    "💵 M3 — Salário vs Custo de Vida",
    "💱 M4 — Kwanza e Câmbio",
    "👩‍👧 M5 — Género e Vulnerabilidade",
    "📖 Metodologia"
])

st.sidebar.markdown("---")
st.sidebar.caption(f"Última actualização: {ultimo['mes'].strftime('%B %Y')}")
st.sidebar.caption("🔬 Dados simulados — fase de desenvolvimento")
st.sidebar.caption("MIT License · Open Source")
st.sidebar.markdown("[📂 GitHub](https://github.com/PrisTheAnalyst/ibea-angola)")

# ─────────────────────────────────────────────
# PÁGINA 1 — VISÃO GERAL
# ─────────────────────────────────────────────

if pagina == "🏠 Visão Geral":

    st.title("🇦🇴 IBEA — Índice de Bem-Estar Económico Angola")
    st.caption("Sistema de Monitorização Económica de Alta Frequência · PrisTheAnalyst")
    st.info("🔬 Fase de desenvolvimento activo — dados simulados. Dados reais de campo integrados na Semana 3.")

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)

    variacao = ultimo["ibea_score"] - penultimo["ibea_score"]
    sinal = "▲" if variacao > 0 else "▼"

    with col1:
        st.metric(
            label="IBEA Score (actual)",
            value=f"{ultimo['ibea_score']:.1f} / 100",
            delta=f"{sinal} {abs(variacao):.1f} vs mês anterior"
        )
    with col2:
        st.metric(
            label="Classificação",
            value=classificacao,
        )
    with col3:
        st.metric(
            label="Cabaz Básico",
            value=f"{ultimo['cabaz_aoa']:,.0f} AOA",
            delta=f"{((ultimo['cabaz_aoa']/df.iloc[0]['cabaz_aoa'])-1)*100:.1f}% vs Jan 2023"
        )
    with col4:
        st.metric(
            label="Poder de Compra Real",
            value=f"{ultimo['poder_compra_pct']:.0f}%",
            delta=f"{ultimo['poder_compra_pct'] - df.iloc[0]['poder_compra_pct']:.1f}pp desde Jan 2023"
        )

    st.markdown("---")

    # Gráfico IBEA histórico
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Evolução do IBEA Score — Jan 2023 a hoje")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["mes"], y=df["ibea_score"],
            mode="lines+markers",
            line=dict(color="#E67E22", width=3),
            marker=dict(size=7),
            name="IBEA Score",
            hovertemplate="<b>%{x|%b %Y}</b><br>IBEA: %{y:.1f}<extra></extra>"
        ))

        # Linhas de referência
        for nivel, label, cor in [
            (75, "Elevado", "#27AE60"),
            (55, "Moderado", "#F1C40F"),
            (35, "Baixo", "#E67E22"),
            (20, "Crítico", "#E74C3C"),
        ]:
            fig.add_hline(y=nivel, line_dash="dot", line_color=cor,
                          annotation_text=label, annotation_position="right")

        fig.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 100], gridcolor="#f0f0f0"),
            xaxis=dict(gridcolor="#f0f0f0"),
            margin=dict(l=0, r=60, t=20, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Contribuição por Módulo")

        modulos_nomes = {
            "m1_inflacao": "M1 Inflação",
            "m2_petroleo": "M2 Petróleo",
            "m3_salario":  "M3 Salário",
            "m4_cambio":   "M4 Câmbio",
            "m5_genero":   "M5 Género"
        }
        pesos = [0.25, 0.20, 0.25, 0.15, 0.15]
        valores_ultimo = [ultimo[m] for m in modulos_nomes.keys()]
        contribuicoes = [v * p for v, p in zip(valores_ultimo, pesos)]

        fig2 = go.Figure(go.Bar(
            x=list(modulos_nomes.values()),
            y=contribuicoes,
            marker_color=["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6"],
            text=[f"{c:.1f}" for c in contribuicoes],
            textposition="outside"
        ))
        fig2.update_layout(
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 30], gridcolor="#f0f0f0"),
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabela resumo
    st.subheader("Scores por Módulo — Mês Actual")
    cols = st.columns(5)
    modulos_info = [
        ("m1_inflacao", "🌽 M1 Inflação",  "25%", "#E74C3C"),
        ("m2_petroleo", "🛢️ M2 Petróleo", "20%", "#3498DB"),
        ("m3_salario",  "💵 M3 Salário",  "25%", "#2ECC71"),
        ("m4_cambio",   "💱 M4 Câmbio",   "15%", "#F39C12"),
        ("m5_genero",   "👩‍👧 M5 Género",  "15%", "#9B59B6"),
    ]
    for col, (chave, nome, peso, cor) in zip(cols, modulos_info):
        with col:
            st.metric(label=f"{nome} ({peso})", value=f"{ultimo[chave]:.1f}")

# ─────────────────────────────────────────────
# PÁGINA 2 — M1 INFLAÇÃO
# ─────────────────────────────────────────────

elif pagina == "🌽 M1 — Inflação Alimentar":

    st.title("🌽 Módulo 1 — Inflação Alimentar (IPA)")
    st.caption("Índice de Preços Alimentares Angola · recolha de campo semanal")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score M1 actual", f"{ultimo['m1_inflacao']:.1f} / 100")
    with col2:
        st.metric("Cabaz básico", f"{ultimo['cabaz_aoa']:,.0f} AOA")
    with col3:
        variacao_cabaz = ((ultimo["cabaz_aoa"] / df.iloc[0]["cabaz_aoa"]) - 1) * 100
        st.metric("Variação desde Jan 2023", f"+{variacao_cabaz:.1f}%")

    st.markdown("---")

    fig = px.line(df, x="mes", y="m1_inflacao",
                  title="Score M1 — Inflação Alimentar (0=pior, 100=melhor)",
                  labels={"mes": "Mês", "m1_inflacao": "Score M1"},
                  color_discrete_sequence=["#E74C3C"])
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("📌 **Como ler este gráfico:** Score baixo = inflação alta = menor bem-estar. A tendência descendente reflecte a pressão inflacionária acumulada em Angola desde 2023.")

    st.subheader("Evolução do Cabaz Básico em AOA")
    fig2 = px.area(df, x="mes", y="cabaz_aoa",
                   labels={"mes": "Mês", "cabaz_aoa": "Custo do Cabaz (AOA)"},
                   color_discrete_sequence=["#E74C3C"])
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# PÁGINA 3 — M3 SALÁRIO
# ─────────────────────────────────────────────

elif pagina == "💵 M3 — Salário vs Custo de Vida":

    st.title("💵 Módulo 3 — Salário Mínimo vs Custo de Vida")
    st.caption("Poder de compra real do trabalhador angolano · 2023–2025")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score M3 actual", f"{ultimo['m3_salario']:.1f} / 100")
    with col2:
        st.metric("Salário mínimo", f"{ultimo['salario_minimo_aoa']:,.0f} AOA")
    with col3:
        st.metric("Cobre o cabaz?", f"{ultimo['poder_compra_pct']:.0f}%",
                  delta=f"{ultimo['poder_compra_pct'] - df.iloc[0]['poder_compra_pct']:.1f}pp")

    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["mes"], y=df["salario_minimo_aoa"],
        name="Salário Mínimo (AOA)",
        line=dict(color="#2ECC71", width=3),
        fill="tozeroy", fillcolor="rgba(46,204,113,0.1)"
    ))
    fig.add_trace(go.Scatter(
        x=df["mes"], y=df["cabaz_aoa"],
        name="Custo do Cabaz Básico (AOA)",
        line=dict(color="#E74C3C", width=3),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.1)"
    ))
    fig.update_layout(
        title="Salário Mínimo vs Custo do Cabaz Básico — Angola",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_title="AOA",
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 Quando a linha vermelha (cabaz) ultrapassa a verde (salário), o trabalhador entra em défice alimentar.")

# ─────────────────────────────────────────────
# PÁGINA METODOLOGIA
# ─────────────────────────────────────────────

elif pagina == "📖 Metodologia":

    st.title("📖 Metodologia IBEA")

    st.markdown("""
    ### Fórmula do Índice
    ```
    IBEA = (M1 × 0.25) + (M2 × 0.20) + (M3 × 0.25) + (M4 × 0.15) + (M5 × 0.15)
    ```
    Cada módulo é normalizado para a escala **0–100** antes da ponderação.
    **Quanto maior o score, maior o bem-estar económico.**

    ### Ponderação e Justificação
    | Módulo | Peso | Justificação |
    |--------|------|-------------|
    | M1 Inflação Alimentar | 25% | Principal determinante de estabilidade social |
    | M2 Petróleo e Economia | 20% | Leading indicator — antecipa inflação em 30–60 dias |
    | M3 Salário vs Custo de Vida | 25% | Poder de compra real — medida directa de bem-estar |
    | M4 Kwanza e Câmbio | 15% | Leading indicator de pressão inflacionária futura |
    | M5 Vulnerabilidade e Género | 15% | Factor de ajuste ESG — captura desigualdades estruturais |

    ### Classificação do Score
    | Score | Classificação |
    |-------|--------------|
    | 75–100 | 🟢 Bem-estar Elevado |
    | 55–74  | 🟡 Bem-estar Moderado |
    | 35–54  | 🟠 Bem-estar Baixo |
    | 20–34  | 🔴 Bem-estar Crítico |
    | 0–19   | ⚫ Situação de Colapso |

    ### Fontes de Dados
    - **Campo próprio:** Recolha semanal em mercados de Luanda
    - **BNA:** Taxa de câmbio oficial
    - **INE Angola:** IPC, salário mínimo, dados populacionais
    - **OPEC:** Preço do Brent e produção angolana
    - **Banco Mundial:** Dados de desenvolvimento e género
    """)

    st.markdown("---")
    st.caption("Código aberto · github.com/PrisTheAnalyst/ibea-angola · MIT License")

# ─────────────────────────────────────────────
# PÁGINAS RESTANTES — placeholder
# ─────────────────────────────────────────────

else:
    st.title(pagina)
    st.info("🚧 Este módulo está em desenvolvimento. Disponível na Semana 5 do roadmap.")
    st.markdown("Acompanha o progresso no [GitHub](https://github.com/PrisTheAnalyst/ibea-angola).")
