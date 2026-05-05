# Metodologia IBEA — Índice de Bem-Estar Económico Angola

## 1. Visão Geral
O IBEA é um índice composto normalizado numa escala de 0 a 100, calculado mensalmente a partir de 6 módulos independentes. Quanto maior o valor, maior o bem-estar económico.

## 2. Fórmula de Cálculo
```
IBEA = (M1 × 0.25) + (M2 × 0.20) + (M3 × 0.25) + (M4 × 0.15) + (M5 × 0.15)
```
Cada módulo é normalizado individualmente para a escala 0–100 antes da ponderação.

## 3. Normalização por Módulo
Fórmula de normalização min-max:
```
Valor_normalizado = ((Valor - Min_histórico) / (Max_histórico - Min_histórico)) × 100
```
Para indicadores negativos (ex: inflação alta = pior bem-estar), a normalização é invertida.

## 4. Ponderação e Justificação

| Módulo     | Peso | Justificação |
|------------|------|-------------|
| M1 Inflação | 25% | Principal determinante de estabilidade social |
| M2 Petróleo | 20% | Leading indicator — antecipa variações em 30-60 dias |
| M3 Salário  | 25% | Poder de compra real — medida directa de bem-estar |
| M4 Câmbio   | 15% | Leading indicator de pressão inflacionária futura |
| M5 Género   | 15% | Factor de ajuste ESG — captura desigualdades estruturais |

## 5. Frequência de Actualização
- **Semanal:** M4 (câmbio paralelo), preços de campo M1
- **Mensal:** Todos os módulos — publicação oficial do IBEA
- **Trimestral:** Revisão de ponderações e metodologia

## 6. Limitações e Transparência
- Os dados do mercado paralelo são estimativas de campo — não dados oficiais
- O módulo M5 está em desenvolvimento activo
- O IBEA é complementar aos dados oficiais do INE e BNA — não os substitui
