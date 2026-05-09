# 💰 SafIA
## Saúde Financeira com Inteligência Artificial

O **SafIA** é uma aplicação desenvolvida em Python com foco em análise financeira pessoal utilizando Inteligência Artificial.

A aplicação permite que o usuário envie extratos ou faturas financeiras em formato CSV/Excel, informe sua renda e gastos fixos mensais, e receba automaticamente:

- análises financeiras;
- visualizações gráficas;
- comparativos mensais;
- categorização automática de gastos;
- insights inteligentes;
- relatório gerado por IA.

---

# 🚀 Objetivo do Projeto

O objetivo do SafIA é transformar dados financeiros em informações úteis para apoiar a organização financeira e a tomada de decisão do usuário.

O sistema foi desenvolvido como MVP acadêmico para demonstrar a integração entre:

- Python;
- análise de dados;
- visualização de dados;
- Inteligência Artificial local com Ollama.

---

# 🧠 Funcionalidades

## 📥 Upload de Extratos/Faturas
O usuário pode enviar arquivos:

- `.csv`
- `.xlsx`

contendo informações financeiras.

---

## 🏷️ Categorização Automática
O sistema identifica automaticamente categorias como:

- Alimentação
- Transporte
- Saúde
- Compras
- Assinaturas
- Lazer
- Viagem
- Outros

---

## 📊 Análise Financeira
O SafIA calcula automaticamente:

- gastos variáveis;
- gastos fixos;
- saldo estimado;
- percentual da renda comprometida;
- maiores categorias de gasto;
- análise mensal;
- comparativo entre meses.

---

## 📈 Visualizações Gráficas

O sistema gera automaticamente:

- gráfico de gastos por categoria;
- distribuição percentual dos gastos;
- evolução dos gastos ao longo dos meses;
- comparativo entre renda e despesas.

---

## 🤖 Relatório Inteligente com IA

O SafIA utiliza um modelo LLM local via **Ollama** para gerar:

- diagnóstico financeiro;
- análise mês a mês;
- comparação de comportamento financeiro;
- pontos de atenção;
- sugestões de economia;
- conclusão financeira geral.

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Backend e lógica |
| Streamlit | Interface web |
| Pandas | Manipulação de dados |
| NumPy | Cálculos e estatísticas |
| Matplotlib | Visualizações |
| Ollama | Execução local de IA |
| OpenAI SDK | Comunicação com o Ollama |

---

# 🖥️ Interface

O sistema roda localmente em:

```bash
http://localhost:8080