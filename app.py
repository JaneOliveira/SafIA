import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ai_report import gerar_relatorio_ia

st.set_page_config(
    page_title="SafIA - Saúde Financeira com IA",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
/* Fundo geral */
.stApp {
    background-color: #F7F8FA;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* Títulos */
h1, h2, h3 {
    color: #16324F;
    font-family: 'Segoe UI', sans-serif;
}

/* Texto padrão */
p, span, div {
    font-family: 'Segoe UI', sans-serif;
}

/* Cards de métricas */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.04);
}

/* Valor das métricas */
div[data-testid="stMetricValue"] {
    color: #1F7A5C;
    font-weight: 700;
}

/* Labels das métricas */
div[data-testid="stMetricLabel"] {
    color: #2E3440;
}

/* Botões */
.stButton > button {
    background-color: #1F7A5C;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #16324F;
    color: white;
}

/* Upload */
section[data-testid="stFileUploader"] {
    background-color: #F7F8FA;
    border: 1px dashed #1F7A5C;
    border-radius: 14px;
    padding: 12px;
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Barra de progresso */
div[data-testid="stProgress"] > div > div > div {
    background-color: #1F7A5C;
}

/* Remove excesso de margem */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Linha divisória suave */
hr {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #16324F 0%, #1F7A5C 100%);
    padding: 32px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
">
    <h1 style="color: white; margin-bottom: 8px;">SafIA</h1>
    <h3 style="color: #E8F5EF; margin-top: 0;">
        Saúde Financeira com Inteligência Artificial
    </h3>
    <p style="font-size: 18px; color: #FFFFFF; max-width: 760px;">
        Clareza para entender seus gastos. Inteligência para melhorar suas decisões.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
O SafIA analisa seus gastos, identifica padrões financeiros e gera insights para apoiar sua saúde financeira.
""")

# -----------------------------
# Funções auxiliares
# -----------------------------

def ler_arquivo(arquivo):
    if arquivo.name.endswith(".csv"):
        return pd.read_csv(arquivo)
    elif arquivo.name.endswith(".xlsx"):
        return pd.read_excel(arquivo)
    else:
        st.error("Formato ainda não suportado. Use CSV ou Excel.")
        return None


def padronizar_colunas(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("ç", "c")
        .str.replace("ã", "a")
    )
    return df


def converter_valor(valor):
    if pd.isna(valor):
        return np.nan

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()
    valor = valor.replace("R$", "").replace(" ", "")

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")
        return pd.to_numeric(valor, errors="coerce")

    return pd.to_numeric(valor, errors="coerce")


def categorizar_gasto(descricao):
    descricao = str(descricao).upper()

    if any(p in descricao for p in ["IFOOD", "RESTAURANTE", "LANCH", "MERCADO", "SUPERMERCADO", "PADARIA", "BAR", "AÇAÍ", "ACAI", "CACAU", "BRUCKS", "SUPER BOM", "GULOSAO"]):
        return "Alimentação"
    elif any(p in descricao for p in ["UBER", "99", "POSTO", "COMBUSTIVEL", "GASOLINA", "PETROBRAS", "PREMMIA"]):
        return "Transporte"
    elif any(p in descricao for p in ["NETFLIX", "SPOTIFY", "AMAZON", "DISNEY", "MAX", "GLOBOPLAY", "GLOBO"]):
        return "Assinaturas"
    elif any(p in descricao for p in ["FARMACIA", "DROGARIA", "MEDICO", "HOSPITAL", "RAIA", "RDSAUDE", "NEURO"]):
        return "Saúde"
    elif any(p in descricao for p in ["SHOPPING", "ROUPA", "MAGAZINE", "AMERICANAS", "MERCADO LIVRE", "BOTICARIO", "SAMSUNG", "MAIA LOJA", "HI PLUS"]):
        return "Compras"
    elif any(p in descricao for p in ["HOTEL", "HOTEIS", "EXPEDIA", "TURISMO"]):
        return "Viagem"
    elif any(p in descricao for p in ["CINEMA", "SHOW", "LAZER"]):
        return "Lazer"
    else:
        return "Outros"


def preparar_dados(df):
    df = padronizar_colunas(df)

    colunas_necessarias = ["data", "descricao", "valor"]

    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            st.error(f"O arquivo precisa ter a coluna: {coluna}")
            return None

    # Mantém as colunas extras da fatura, se existirem
    colunas_base = ["data", "descricao", "valor"]

    colunas_opcionais = [
        "mes_fatura",
        "vencimento_fatura",
        "emissao_fatura",
        "arquivo_origem",
        "cartao"
    ]

    colunas_para_manter = colunas_base + [
        coluna for coluna in colunas_opcionais if coluna in df.columns
    ]

    df = df[colunas_para_manter].copy()

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["valor"] = df["valor"].apply(converter_valor)

    if "vencimento_fatura" in df.columns:
        df["vencimento_fatura"] = pd.to_datetime(
            df["vencimento_fatura"],
            errors="coerce",
            dayfirst=True
        )

    if "emissao_fatura" in df.columns:
        df["emissao_fatura"] = pd.to_datetime(
            df["emissao_fatura"],
            errors="coerce",
            dayfirst=True
        )

    df = df.dropna(subset=["data", "descricao", "valor"])
    df = df.drop_duplicates()

    # Prioridade para definir o mês de análise:
    # 1. mês da fatura
    # 2. vencimento da fatura
    # 3. emissão da fatura
    # 4. data da compra
    if "mes_fatura" in df.columns:
        df["mes"] = df["mes_fatura"].astype(str)

    elif "vencimento_fatura" in df.columns:
        df["mes"] = df["vencimento_fatura"].dt.to_period("M").astype(str)

    elif "emissao_fatura" in df.columns:
        df["mes"] = df["emissao_fatura"].dt.to_period("M").astype(str)

    else:
        df["mes"] = df["data"].dt.to_period("M").astype(str)

    df["categoria"] = df["descricao"].apply(categorizar_gasto)

    return df


def gerar_grafico_barras(df_categoria):
    fig, ax = plt.subplots()
    ax.bar(df_categoria["categoria"], df_categoria["valor"])
    ax.set_title("Gastos por Categoria")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Valor gasto")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


def gerar_grafico_linha(df_mes):
    fig, ax = plt.subplots()
    ax.plot(df_mes["mes"], df_mes["valor"], marker="o")
    ax.set_title("Evolução dos Gastos Variáveis por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor gasto")
    plt.xticks(rotation=45)
    st.pyplot(fig)


def gerar_grafico_pizza(df_categoria):
    fig, ax = plt.subplots()
    ax.pie(df_categoria["valor"], labels=df_categoria["categoria"], autopct="%1.1f%%")
    ax.set_title("Distribuição dos Gastos")
    st.pyplot(fig)


def gerar_grafico_renda_gastos(df_analise_mes):
    fig, ax = plt.subplots()
    ax.plot(df_analise_mes["mes"], df_analise_mes["renda"], marker="o", label="Renda")
    ax.plot(df_analise_mes["mes"], df_analise_mes["total_geral"], marker="o", label="Gastos totais")
    ax.set_title("Renda x Gastos Totais por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("📥 Entrada de Dados")

arquivo = st.sidebar.file_uploader(
    "Envie sua fatura ou extrato em CSV ou Excel",
    type=["csv", "xlsx"]
)

st.sidebar.header("💵 Renda Mensal")

renda_mensal = st.sidebar.number_input(
    "Informe sua renda mensal",
    min_value=0.0,
    value=3000.0,
    step=100.0
)

st.sidebar.header("🏠 Gastos Fixos Mensais")

aluguel = st.sidebar.number_input("Aluguel", min_value=0.0, value=0.0)
luz = st.sidebar.number_input("Luz", min_value=0.0, value=0.0)
agua = st.sidebar.number_input("Água", min_value=0.0, value=0.0)
internet = st.sidebar.number_input("Internet", min_value=0.0, value=0.0)
planos = st.sidebar.number_input("Planos / Assinaturas fixas", min_value=0.0, value=0.0)
outros_fixos = st.sidebar.number_input("Outros gastos fixos", min_value=0.0, value=0.0)

gastos_fixos_mensais = aluguel + luz + agua + internet + planos + outros_fixos

gerar = st.sidebar.button("Gerar Relatório")

# -----------------------------
# Processamento
# -----------------------------

if gerar:
    if arquivo is None:
        st.warning("Envie um arquivo CSV ou Excel para gerar o relatório.")
    else:
        df_original = ler_arquivo(arquivo)

        if df_original is not None:
            df = preparar_dados(df_original)

            if df is not None and not df.empty:
                st.success("Arquivo processado com sucesso!")

                qtd_meses = df["mes"].nunique()

                total_variavel = df["valor"].sum()
                renda_total_periodo = renda_mensal * qtd_meses
                gastos_fixos_periodo = gastos_fixos_mensais * qtd_meses
                total_geral = total_variavel + gastos_fixos_periodo
                saldo = renda_total_periodo - total_geral

                percentual_comprometido = 0
                if renda_total_periodo > 0:
                    percentual_comprometido = (total_geral / renda_total_periodo) * 100

                df_categoria = (
                    df.groupby("categoria", as_index=False)["valor"]
                    .sum()
                    .sort_values("valor", ascending=False)
                )

                df_mes = (
                    df.groupby("mes", as_index=False)["valor"]
                    .sum()
                    .sort_values("mes")
                )

                maior_categoria = df_categoria.iloc[0]["categoria"]
                valor_maior_categoria = df_categoria.iloc[0]["valor"]

                # -----------------------------
                # Análise mensal
                # -----------------------------

                df_analise_mes = df_mes.copy()
                df_analise_mes = df_analise_mes.rename(columns={"valor": "gastos_variaveis"})

                df_analise_mes["gastos_fixos"] = gastos_fixos_mensais
                df_analise_mes["renda"] = renda_mensal
                df_analise_mes["total_geral"] = (
                    df_analise_mes["gastos_variaveis"] + df_analise_mes["gastos_fixos"]
                )
                df_analise_mes["saldo"] = df_analise_mes["renda"] - df_analise_mes["total_geral"]

                df_analise_mes["percentual_comprometido"] = np.where(
                    df_analise_mes["renda"] > 0,
                    (df_analise_mes["total_geral"] / df_analise_mes["renda"]) * 100,
                    0
                )

                # -----------------------------
                # Comparativo entre categorias
                # -----------------------------

                comparacao_categoria = (
                    df.groupby(["mes", "categoria"])["valor"]
                    .sum()
                    .reset_index()
                )

                pivot_categoria = comparacao_categoria.pivot(
                    index="categoria",
                    columns="mes",
                    values="valor"
                ).fillna(0)

                meses = list(pivot_categoria.columns)

                maiores_aumentos_texto = "Não há meses suficientes para comparação."
                maiores_reducoes_texto = "Não há meses suficientes para comparação."

                if len(meses) >= 2:
                    ultimo_mes = meses[-1]
                    penultimo_mes = meses[-2]

                    pivot_categoria["diferenca"] = (
                        pivot_categoria[ultimo_mes] - pivot_categoria[penultimo_mes]
                    )

                    maiores_aumentos = (
                        pivot_categoria[pivot_categoria["diferenca"] > 0]
                        .sort_values("diferenca", ascending=False)
                        .head(5)
                    )

                    maiores_reducoes = (
                        pivot_categoria[pivot_categoria["diferenca"] < 0]
                        .sort_values("diferenca", ascending=True)
                        .head(5)
                    )

                    maiores_aumentos_texto = maiores_aumentos["diferenca"].to_string()
                    maiores_reducoes_texto = maiores_reducoes["diferenca"].to_string()

                # -----------------------------
                # Cards principais
                # -----------------------------

                st.header("Resumo Financeiro do Período")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    f"Renda no período ({qtd_meses} meses)",
                    f"R$ {renda_total_periodo:,.2f}"
                )
                col2.metric("Gastos variáveis", f"R$ {total_variavel:,.2f}")
                col3.metric("Gastos fixos no período", f"R$ {gastos_fixos_periodo:,.2f}")
                col4.metric("Saldo estimado", f"R$ {saldo:,.2f}")

                st.metric(
                    "Percentual da renda comprometida no período",
                    f"{percentual_comprometido:.1f}%"
                )

                # -----------------------------
                # Alertas
                # -----------------------------

                st.header("Diagnóstico Financeiro")

                if percentual_comprometido >= 90:
                    st.error("Sua renda está muito comprometida no período analisado.")
                elif percentual_comprometido >= 70:
                    st.warning("Uma parte relevante da renda está comprometida.")
                else:
                    st.success("O comprometimento da renda está em um nível mais confortável.")

                if saldo < 0:
                    st.error("O saldo estimado do período está negativo.")
                elif saldo < renda_total_periodo * 0.1:
                    st.warning("A sobra financeira do período está baixa.")
                else:
                    st.success("Existe uma margem positiva entre renda e gastos.")

                st.info(
                    f"A maior categoria de gasto foi **{maior_categoria}**, com aproximadamente R$ {valor_maior_categoria:,.2f}."
                )

                # -----------------------------
                # Análise por mês
                # -----------------------------

                st.header("📅 Análise Mensal")

                for _, row in df_analise_mes.iterrows():
                    st.subheader(f"📆 {row['mes']}")

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric("Renda", f"R$ {row['renda']:,.2f}")
                    c2.metric("Gastos variáveis", f"R$ {row['gastos_variaveis']:,.2f}")
                    c3.metric("Gastos totais", f"R$ {row['total_geral']:,.2f}")
                    c4.metric("Saldo", f"R$ {row['saldo']:,.2f}")

                    st.progress(
                        min(row["percentual_comprometido"] / 100, 1.0),
                        text=f"Comprometimento da renda: {row['percentual_comprometido']:.1f}%"
                    )

                    if row["saldo"] < 0:
                        st.error("Neste mês, os gastos ultrapassaram a renda.")
                    elif row["percentual_comprometido"] >= 90:
                        st.warning("Neste mês, a renda ficou quase totalmente comprometida.")
                    elif row["percentual_comprometido"] >= 70:
                        st.warning("Neste mês, o comprometimento foi moderado/alto.")
                    else:
                        st.success("Neste mês, a situação ficou mais confortável.")

                st.subheader("Tabela mensal consolidada")
                st.dataframe(df_analise_mes)

                # -----------------------------
                # Comparativo entre meses
                # -----------------------------

                st.header("📊 Comparativo entre Meses")

                st.subheader("Gastos por categoria ao longo dos meses")
                st.dataframe(pivot_categoria)

                if len(meses) >= 2:
                    st.subheader(f"📈 Aumentos de {penultimo_mes} para {ultimo_mes}")

                    if maiores_aumentos.empty:
                        st.write("Nenhuma categoria teve aumento no último mês.")
                    else:
                        for categoria, row in maiores_aumentos.iterrows():
                            st.write(f"**{categoria}** aumentou R$ {row['diferenca']:,.2f}")

                    st.subheader(f"📉 Reduções de {penultimo_mes} para {ultimo_mes}")

                    if maiores_reducoes.empty:
                        st.write("Nenhuma categoria teve redução no último mês.")
                    else:
                        for categoria, row in maiores_reducoes.iterrows():
                            st.write(f"**{categoria}** reduziu R$ {abs(row['diferenca']):,.2f}")

                # -----------------------------
                # Visualizações
                # -----------------------------

                st.header("📈 Visualizações")

                col_g1, col_g2 = st.columns(2)

                with col_g1:
                    gerar_grafico_barras(df_categoria)

                with col_g2:
                    gerar_grafico_pizza(df_categoria)

                gerar_grafico_linha(df_mes)
                gerar_grafico_renda_gastos(
                    df_analise_mes.rename(columns={"gastos_variaveis": "valor"})
                )

                # -----------------------------
                # Tabelas
                # -----------------------------

                st.header("📋 Dados Consolidados")

                st.subheader("Gastos por Categoria")
                st.dataframe(df_categoria)

                st.subheader("Gastos por Mês")
                st.dataframe(df_mes)

                st.subheader("Transações tratadas")
                st.dataframe(df)

                # -----------------------------
                # Relatório com IA
                # -----------------------------

                st.header("Parecer Inteligente SafIA")

                resumo_financeiro = {
                    "qtd_meses": qtd_meses,
                    "renda_mensal": renda_mensal,
                    "renda_total_periodo": renda_total_periodo,
                    "total_variavel": total_variavel,
                    "gastos_fixos_mensais": gastos_fixos_mensais,
                    "gastos_fixos_periodo": gastos_fixos_periodo,
                    "total_geral": total_geral,
                    "saldo": saldo,
                    "percentual_comprometido": percentual_comprometido,
                    "maior_categoria": maior_categoria,
                    "valor_maior_categoria": valor_maior_categoria,
                    "categorias": df_categoria.to_string(index=False),
                    "analise_mensal": df_analise_mes.to_string(index=False),
                    "comparativo_categorias": pivot_categoria.to_string(),
                    "maiores_aumentos": maiores_aumentos_texto,
                    "maiores_reducoes": maiores_reducoes_texto,
                }

                with st.spinner("Gerando relatório com IA..."):
                    relatorio_ia = gerar_relatorio_ia(resumo_financeiro)

                st.markdown(relatorio_ia)

            else:
                st.error("Não foi possível processar os dados do arquivo.")
else:
    st.info("Envie seus dados financeiros na barra lateral e clique em **Gerar Relatório**.")