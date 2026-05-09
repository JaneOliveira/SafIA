from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODELO = "llama3.2"


def gerar_relatorio_ia(resumo_financeiro: dict) -> str:
    """
    Gera relatório financeiro usando Ollama.
    """

    prompt = f"""
Você é o SafIA, um assistente de saúde financeira pessoal.

Sua tarefa é analisar os dados financeiros abaixo e gerar um relatório claro, útil e educativo.
Não invente valores. Use apenas os dados fornecidos.

DADOS GERAIS DO PERÍODO:
- Quantidade de meses analisados: {resumo_financeiro.get("qtd_meses", 0)}
- Renda mensal informada: R$ {resumo_financeiro.get("renda_mensal", 0):,.2f}
- Renda total do período: R$ {resumo_financeiro.get("renda_total_periodo", 0):,.2f}
- Gastos variáveis no período: R$ {resumo_financeiro.get("total_variavel", 0):,.2f}
- Gastos fixos mensais: R$ {resumo_financeiro.get("gastos_fixos_mensais", 0):,.2f}
- Gastos fixos no período: R$ {resumo_financeiro.get("gastos_fixos_periodo", 0):,.2f}
- Total geral de despesas: R$ {resumo_financeiro.get("total_geral", 0):,.2f}
- Saldo estimado no período: R$ {resumo_financeiro.get("saldo", 0):,.2f}
- Percentual da renda comprometida no período: {resumo_financeiro.get("percentual_comprometido", 0):.1f}%
- Maior categoria de gasto: {resumo_financeiro.get("maior_categoria", "Não identificado")}
- Valor da maior categoria: R$ {resumo_financeiro.get("valor_maior_categoria", 0):,.2f}

GASTOS POR CATEGORIA:
{resumo_financeiro.get("categorias", "")}

ANÁLISE MENSAL:
{resumo_financeiro.get("analise_mensal", "")}

COMPARATIVO ENTRE CATEGORIAS POR MÊS:
{resumo_financeiro.get("comparativo_categorias", "")}

CATEGORIAS QUE MAIS AUMENTARAM:
{resumo_financeiro.get("maiores_aumentos", "")}

CATEGORIAS QUE MAIS REDUZIRAM:
{resumo_financeiro.get("maiores_reducoes", "")}

Gere um relatório em português do Brasil com as seguintes seções:

## 1. Resumo geral
Explique a situação financeira geral do período.

## 2. Análise mês a mês
Comente cada mês de forma simples, considerando renda, gastos totais, saldo e comprometimento.

## 3. Comparativo entre meses
Explique quais gastos aumentaram, quais reduziram e o que isso pode indicar.

## 4. Principais pontos de atenção
Liste os riscos ou comportamentos financeiros que merecem cuidado.

## 5. Dicas práticas de economia
Dê recomendações realistas e acionáveis.

## 6. Diagnóstico final
Finalize com uma conclusão objetiva sobre a saúde financeira.

Use uma linguagem amigável, clara e sem julgamento.
"""

    try:
        resposta = client.chat.completions.create(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente financeiro educativo. "
                        "Responda sempre em português do Brasil. "
                        "Não dê recomendações de investimento específicas. "
                        "Foque em organização financeira, economia e consciência de gastos."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return resposta.choices[0].message.content

    except Exception as erro:
        return f"""
## Relatório SafIA

Não foi possível gerar o relatório com IA no momento.

Erro encontrado:

`{erro}`

### Relatório automático

Com base nos dados informados, recomenda-se observar:

- o percentual da renda comprometida;
- os meses em que os gastos ultrapassaram a renda;
- as categorias com maior crescimento;
- os gastos recorrentes que podem ser reduzidos;
- a possibilidade de criar uma margem mensal para reserva financeira.

Revise principalmente a categoria de maior gasto e os meses com saldo negativo.
"""