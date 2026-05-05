"""
IBEA Calculator v1 — Índice de Bem-Estar Económico Angola
Calcula o score IBEA composto a partir dos 5 módulos
Autora: PrisTheAnalyst
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# PESOS DOS MÓDULOS (soma = 1.0)
# ─────────────────────────────────────────────

IBEA_WEIGHTS = {
    "m1_inflacao": 0.25,
    "m2_petroleo": 0.20,
    "m3_salario":  0.25,
    "m4_cambio":   0.15,
    "m5_genero":   0.15,
}

# ─────────────────────────────────────────────
# DADOS SIMULADOS DOS 5 MÓDULOS (18 meses)
# ─────────────────────────────────────────────

np.random.seed(42)
meses = pd.date_range(start="2023-01-01", periods=18, freq="MS")

def simular_modulo(base, tendencia, ruido):
    """Simula uma série mensal realista."""
    return np.round(
        base + np.cumsum(np.random.uniform(-ruido, tendencia, 18)), 1
    ).clip(0, 100)

modulos_df = pd.DataFrame({
    "mes":        meses,
    # M1: inflação sobe → bem-estar desce → score baixo
    "m1_inflacao": simular_modulo(65, -0.8, 2),
    # M2: petróleo volátil
    "m2_petroleo": simular_modulo(55, -0.3, 3),
    # M3: salário perde poder de compra → score cai
    "m3_salario":  simular_modulo(50, -1.0, 1.5),
    # M4: kwanza desvaloriza → score cai
    "m4_cambio":   simular_modulo(48, -0.5, 2.5),
    # M5: vulnerabilidade género — relativamente estável
    "m5_genero":   simular_modulo(42, -0.2, 1),
})

# ─────────────────────────────────────────────
# FUNÇÕES DO CALCULADOR
# ─────────────────────────────────────────────

def normalizar_modulo(valor, min_hist, max_hist, inverter=False):
    """Normaliza valor para escala 0–100."""
    if max_hist == min_hist:
        return 50.0
    n = ((valor - min_hist) / (max_hist - min_hist)) * 100
    return round(100 - n if inverter else n, 2)


def calcular_ibea(modulos: dict) -> dict:
    """
    Input : dicionário com scores 0–100 de cada módulo
    Output: score IBEA, classificação e breakdown
    """
    score = sum(modulos.get(m, 0) * p for m, p in IBEA_WEIGHTS.items())
    return {
        "ibea_score":    round(score, 2),
        "classificacao": classificar_ibea(score),
        "breakdown": {
            m: {
                "valor":       modulos.get(m, 0),
                "peso":        p,
                "contribuicao": round(modulos.get(m, 0) * p, 2)
            }
            for m, p in IBEA_WEIGHTS.items()
        }
    }


def classificar_ibea(score: float) -> str:
    if score >= 75:   return "🟢 Bem-estar Elevado"
    elif score >= 55: return "🟡 Bem-estar Moderado"
    elif score >= 35: return "🟠 Bem-estar Baixo"
    elif score >= 20: return "🔴 Bem-estar Crítico"
    else:             return "⚫ Situação de Colapso"


def calcular_serie_ibea(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o IBEA para cada mês do DataFrame."""
    resultados = []
    for _, row in df.iterrows():
        modulos = {m: row[m] for m in IBEA_WEIGHTS.keys()}
        r = calcular_ibea(modulos)
        resultados.append({
            "mes":             row["mes"],
            "ibea_score":      r["ibea_score"],
            "classificacao":   r["classificacao"],
            "m1_inflacao":     row["m1_inflacao"],
            "m2_petroleo":     row["m2_petroleo"],
            "m3_salario":      row["m3_salario"],
            "m4_cambio":       row["m4_cambio"],
            "m5_genero":       row["m5_genero"],
        })
    return pd.DataFrame(resultados)


# ─────────────────────────────────────────────
# EXECUÇÃO DIRECTA — gera e exporta o CSV do IBEA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    ibea_serie = calcular_serie_ibea(modulos_df)
    os.makedirs("data", exist_ok=True)
    ibea_serie.to_csv("data/ibea_historico.csv", index=False)

    ultimo = ibea_serie.iloc[-1]
    print("✅ IBEA calculado com sucesso!")
    print(f"   Período          : {ibea_serie['mes'].iloc[0].strftime('%b %Y')} → {ultimo['mes'].strftime('%b %Y')}")
    print(f"   IBEA mais recente: {ultimo['ibea_score']} — {ultimo['classificacao']}")
    print(f"   Mínimo histórico : {ibea_serie['ibea_score'].min()}")
    print(f"   Máximo histórico : {ibea_serie['ibea_score'].max()}")
    print(f"   Ficheiro gerado  : data/ibea_historico.csv")
