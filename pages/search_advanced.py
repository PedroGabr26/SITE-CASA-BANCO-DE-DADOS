import streamlit as st
import requests

# Função para realizar a requisição à API
def fazer_requisicao(filtros):
    url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"
    headers = {
        "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
    }

    # Corpo da requisição com os filtros
    body = {}

    # Adicionando filtros no corpo da requisição
    if filtros['estado']:
        body['estado'] = filtros['estado']
    if filtros['situacao_cadastral']:
        body['situacao_cadastral'] = filtros['situacao_cadastral']
    if filtros['codigo_atividade_principal']:
        body['codigo_atividade_principal'] = filtros['codigo_atividade_principal']
    if filtros['data_abertura_inicio'] and filtros['data_abertura_fim']:
        body['data_abertura'] = {
            "inicio": filtros['data_abertura_inicio'],
            "fim": filtros['data_abertura_fim']
        }
    if filtros['capital_social_minimo'] and filtros['capital_social_maximo']:
        body['capital_social'] = {
            "minimo": filtros['capital_social_minimo'],
            "maximo": filtros['capital_social_maximo']
        }

    # Realizando a requisição
    response = requests.post(url, headers=headers, json=body)

    # Verificando a resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": response.status_code}

# Interface com Streamlit
def app():
    st.title("Busca Avançada CNPJ")

    # Campos de input para os filtros
    estado = st.text_input("Estado (ex: SP)", "")
    situacao_cadastral = st.selectbox("Situação Cadastral", ["", "ATIVA", "INATIVA"])
    codigo_atividade_principal = st.text_input("Código Atividade Principal (ex: 7020400)", "")
    data_abertura_inicio = st.date_input("Data Abertura - Início", None)
    data_abertura_fim = st.date_input("Data Abertura - Fim", None)
    capital_social_minimo = st.number_input("Capital Social Mínimo", min_value=0, step=1000, value=10000)
    capital_social_maximo = st.number_input("Capital Social Máximo", min_value=0, step=1000, value=500000)

    # Criando o dicionário de filtros
    filtros = {
        "estado": [estado] if estado else None,
        "situacao_cadastral": [situacao_cadastral] if situacao_cadastral else None,
        "codigo_atividade_principal": [codigo_atividade_principal] if codigo_atividade_principal else None,
        "data_abertura_inicio": data_abertura_inicio if data_abertura_inicio else None,
        "data_abertura_fim": data_abertura_fim if data_abertura_fim else None,
        "capital_social_minimo": capital_social_minimo if capital_social_minimo else None,
        "capital_social_maximo": capital_social_maximo if capital_social_maximo else None,
    }

    # Botão para realizar a busca
    if st.button("Buscar"):
        # Fazer a requisição com os filtros
        resultados = fazer_requisicao(filtros)

        # Exibindo os resultados
        if "erro" in resultados:
            st.error(f"Erro na requisição: {resultados['erro']}")
        else:
            st.write(resultados)

# Rodar a aplicação
if __name__ == "__main__":
    app()