import streamlit as st
import requests

st.title("Busca Avançada CNPJ")

# Função para realizar a requisição à API
def fazer_requisicao(filtros):
    url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"
    headers = {
        "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
    }

    # Corpo da requisição com os filtros
    body = {}

    # Adicionando filtros no corpo da requisição, apenas se houver valores
    if filtros.get('nome_empresa'):
        body['nome_empresa'] = filtros['nome_empresa']
    if filtros.get('estado'):
        body['estado'] = filtros['estado']
    if filtros.get('municipio'):
        body['municipio'] = filtros['municipio']
    if filtros.get('situacao_cadastral'):
        body['situacao_cadastral'] = filtros['situacao_cadastral']
    if filtros.get('codigo_atividade_principal'):
        body['codigo_atividade_principal'] = filtros['codigo_atividade_principal']
    
    # Se as datas de abertura não forem fornecidas, define o valor padrão "2025-01-12"
    if filtros.get('data_abertura_inicio') and filtros.get('data_abertura_fim'):
        body['data_abertura'] = {
            "inicio": filtros['data_abertura_inicio'],
            "fim": filtros['data_abertura_fim'],
            "ultimos_dias": 0
        }
    else:
        body['data_abertura'] = {
            "inicio": "2025-01-12",
            "fim": "2025-01-12",
            "ultimos_dias": 0
        }

    if filtros.get('capital_social_minimo') and filtros.get('capital_social_maximo'):
        body['capital_social'] = {
            "minimo": filtros['capital_social_minimo'],
            "maximo": filtros['capital_social_maximo']
        }

    # Se não houver filtros, o corpo da requisição será vazio
    if not body:
        body = {}

    # Realizando a requisição
    response = requests.post(url, headers=headers, json=body)

    # Verificando a resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": response.status_code}

# Interface com Streamlit
def app():
    # Campos de input para os filtros
    nome_empresa = st.text_input("Nome da Empresa", "")
    estado = st.text_input("Estado (ex: SP)", "")
    municipio = st.text_input("Município (ex: Guarulhos)", "")  # Adicionando o campo Município
    situacao_cadastral = st.selectbox("Situação Cadastral", ["", "ATIVA", "INAPTA"])
    codigo_atividade_principal = st.text_input("Código Atividade Principal (ex: 7020400)", "")
    data_abertura_inicio = st.date_input("Data Abertura - Início", None)
    data_abertura_fim = st.date_input("Data Abertura - Fim", None)
    capital_social_minimo = st.number_input("Capital Social Mínimo", min_value=0, step=1000, value=0)
    capital_social_maximo = st.number_input("Capital Social Máximo", min_value=0, step=1000, value=0)

    # Ajustando as datas de abertura para "2025-01-12" se não forem informadas
    if not data_abertura_inicio and not data_abertura_fim:
        data_abertura_inicio = "1920-01-12"
        data_abertura_fim = "2025-01-12"

    # Criando o dicionário de filtros, ignorando valores vazios
    filtros = {
        "nome_empresa": [nome_empresa] if nome_empresa else None,
        "estado": [estado] if estado else None,
        "municipio": [municipio] if municipio else None,  # Adicionando município como lista
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
