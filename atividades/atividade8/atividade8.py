import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chisquare

df = pd.read_csv("customers-10000.csv")

# 1. Região
paises = df["Country"].value_counts()
cidades = df["City"].value_counts()
print("Top país:", paises.index[0], paises.iloc[0], "| média por país:", round(paises.mean(), 1))
print("Cidades empatadas no topo (4 clientes):", (cidades == cidades.max()).sum())
print("Teste qui-quadrado (países uniformes?):", chisquare(paises))
top10 = paises.head(10).sort_values()
plt.figure(figsize=(9, 5))
plt.barh(top10.index, top10.values, color="#4C78A8")
plt.axvline(paises.mean(), color="gray", ls="--", label=f"Média por país ({paises.mean():.0f})")
plt.title("Top 10 países por número de clientes"); plt.xlabel("Clientes"); plt.ylabel("País")
plt.legend(); plt.tight_layout(); plt.savefig("grafico1_top10_paises.png", dpi=150); plt.close()

# 2. Datas
df["Subscription Date"] = pd.to_datetime(df["Subscription Date"])
print(df["Subscription Date"].min(), "→", df["Subscription Date"].max())
print(df["Subscription Date"].dt.year.value_counts().sort_index())
mensal = df.groupby(df["Subscription Date"].dt.to_period("M")).size()
# média por mês-calendário corrigida pelo nº de vezes que o mês aparece na base
por_mes = df.groupby(df["Subscription Date"].dt.month).size()
ocorr = mensal.groupby(mensal.index.month).size()
print((por_mes / ocorr).round(0))
print("Teste qui-quadrado (meses uniformes?):", chisquare(mensal))
plt.figure(figsize=(11, 5))
plt.plot(mensal.index.to_timestamp(), mensal.values, marker="o", color="#4C78A8")
plt.axhline(mensal.mean(), color="gray", ls="--", label=f"Média mensal ({mensal.mean():.0f})")
plt.ylim(0, mensal.max() * 1.15)
plt.title("Evolução mensal de assinaturas (jan/2020 – mai/2022)"); plt.xlabel("Mês"); plt.ylabel("Assinaturas")
plt.legend(); plt.tight_layout(); plt.savefig("grafico2_evolucao_mensal.png", dpi=150); plt.close()

# 3. Maior cliente B2B
empresas = df["Company"].value_counts()
print(empresas.head(5))
print("Empresas distintas:", empresas.size, "| empresas com 1 só assinatura:", (empresas == 1).sum(),
      "| empatadas no máximo:", (empresas == empresas.max()).sum())
print(empresas.value_counts().sort_index())
top5 = empresas.head(5)
plt.figure(figsize=(8, 4.5))
plt.bar(top5.index, top5.values, color="#4C78A8")
plt.title("Top 5 empresas por nº de assinaturas"); plt.xlabel("Empresa"); plt.ylabel("Assinaturas")
plt.tight_layout(); plt.savefig("grafico3_top5_empresas.png", dpi=150); plt.close()
