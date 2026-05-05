"""
IBEA — Pipeline v1
Ponto 3: Gera dados simulados, calcula IPA e exporta CSV limpo
Autora: PrisTheAnalyst
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# PASSO 1 — Simula preços do cabaz básico
#           (substituirás por dados reais de campo)
# ─────────────────────────────────────────────

np.random.seed(42)

meses = pd.date_range(start="2023-01-01", periods=18, freq="MS")

# Preços em AOA — com tendência de subida (inflação real de Angola)
dados = {
    "mes":            meses,
    "funge_kg":       np.round(300  + np.cumsum(np.random.uniform(5, 20, 18)), 1),
    "arroz_kg":       np.round(700  + np.cumsum(np.random.uniform(8, 25, 18)), 1),
    "oleo_litro":     np.round(1200 + np.cumsum(np.random.uniform(10, 40, 18)), 1),
    "pao_unidade":    np.round(150  + np.cumsum(np.random.uniform(2, 8,  18)), 1),
    "frango_kg":      np.round(2000 + np.cumsum(np.random.uniform(20, 60, 18)), 1),
    "peixe_kg":       np.round(1500 + np.cumsum(np.random.uniform(15, 50, 18)), 1),
    "feijao_kg":      np.round(500  + np.cumsum(np.random.uniform(5, 18,  18)), 1),
    "acucar_kg":      np.round(400  + np.cumsum(np.random.uniform(4, 15,  18)), 1),
}

df = pd.DataFrame(dados)

# ─────────────────────────────────────────────
# PASSO 2 — Calcula o IPA (Índice de Preços Alimentares Angola)
# ─────────────────────────────────────────────

# Custo total do cabaz por mês
df["cabaz_total_aoa"] = (
    df["funge_kg"]    * 2 +   # 2 kg por mês
    df["arroz_kg"]    * 2 +
    df["oleo_litro"]  * 1 +
    df["pao_unidade"] * 30 +  # 1 pão por dia
    df["frango_kg"]   * 1 +
    df["peixe_kg"]    * 1 +
    df["feijao_kg"]   * 1 +
    df["acucar_kg"]   * 1
)

# IPA: variação percentual acumulada desde Jan 2023 (base = 100)
df["ipa_score"] = (df["cabaz_total_aoa"] / df["cabaz_total_aoa"].iloc[0]) * 100
df["ipa_score"] = df["ipa_score"].round(2)

# Variação mensal em %
df["variacao_mensal_pct"] = df["cabaz_total_aoa"].pct_change() * 100
df["variacao_mensal_pct"] = df["variacao_mensal_pct"].round(2)

# ─────────────────────────────────────────────
# PASSO 3 — Exporta CSV limpo para a pasta data/
# ─────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
df.to_csv("data/ipa_historico.csv", index=False)

print("✅ Pipeline concluído com sucesso!")
print(f"   Meses processados : {len(df)}")
print(f"   Cabaz Jan 2023    : {df['cabaz_total_aoa'].iloc[0]:,.0f} AOA")
print(f"   Cabaz mais recente: {df['cabaz_total_aoa'].iloc[-1]:,.0f} AOA")
print(f"   IPA actual        : {df['ipa_score'].iloc[-1]:.1f} (base 100 = Jan 2023)")
print(f"   Ficheiro gerado   : data/ipa_historico.csv")
