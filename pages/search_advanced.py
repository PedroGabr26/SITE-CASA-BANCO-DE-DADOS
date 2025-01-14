import streamlit as st
import requests
import pandas as pd

st.title("Busca Avançada CNPJ")

# Função para realizar a requisição à API
def fazer_requisicao(filtros):
    url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"
    headers = {
        "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
    }

    # Corpo da requisição com os filtros
    body = {}

    # Adicionando filtros no corpo da requisição, com formato de lista
    if filtros.get('cnpj'):
        body['cnpj'] = filtros['cnpj']
    if filtros.get('estado'):
        body['uf'] = filtros['estado']
    if filtros.get('bairro'):
        body['bairro'] = filtros['bairro']
    if filtros.get('ddd'):
        body['ddd'] = filtros['ddd']
    if filtros.get('nome_empresa'):
        body['nome_empresa'] = filtros['nome_empresa']
    if filtros.get('municipio'):
        body['municipio'] = filtros['municipio']
    if filtros.get('situacao_cadastral'):
        body['situacao_cadastral'] = filtros['situacao_cadastral']
    if filtros.get('codigo_atividade_principal'):
        body['codigo_atividade_principal'] = filtros['codigo_atividade_principal']
    if filtros.get('data_abertura_inicio') and filtros.get('data_abertura_fim'):
        body['data_abertura'] = {
            "inicio": filtros['data_abertura_inicio'],
            "fim": filtros['data_abertura_fim'],
            "ultimos_dias": 0
        }
    if filtros.get('capital_social_minimo') is not None and filtros.get('capital_social_maximo') is not None:
        body['capital_social'] = {
            "minimo": filtros['capital_social_minimo'],
            "maximo": filtros['capital_social_maximo']
        }
    elif filtros.get('capital_social_minimo') is None and filtros.get('capital_social_maximo') is None:
        body['capital_social'] = {
            "minimo": 0,
            "maximo": 0
        }

    # Realizando a requisição
    response = requests.post(url, headers=headers, json=body)

    # Verificando a resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": response.status_code}

# Função para formatar a data
def formatar_data(data):
    return pd.to_datetime(data).strftime('%d/%m/%Y') if data else "N/A"

# Interface com Streamlit
def app():
    # Campos de input para os filtros
    cnpj = st.text_input("CNPJ", "")
    estado = st.text_input("Estado", "")
    bairro = st.text_input("Bairro", "")
    ddd = st.text_input("DDD ", "")
    nome_empresa = st.text_input("Nome da Empresa", "")
    municipio = st.text_input("Município", "")
    situacao_cadastral = st.selectbox("Situação Cadastral", ["", "ATIVA", "INAPTA", "BAIXADA", "NULA", "SUSPENSA"])
    codigo_atividade_principal = st.text_input("Código Atividade Principal", "")
    data_abertura_inicio = st.date_input("Data Abertura - Início", None)
    data_abertura_fim = st.date_input("Data Abertura - Fim", None)
    capital_social_minimo = st.number_input("Capital Social Mínimo", min_value=0, step=1000, value=0)
    capital_social_maximo = st.number_input("Capital Social Máximo", min_value=0, step=1000, value=0)

    # Criando o dicionário de filtros, ignorando valores vazios
    filtros = {
        "cnpj": [x.strip() for x in cnpj.split(',')] if cnpj else None,
        "estado": [x.strip() for x in estado.split(',')] if estado else None,
        "bairro": [x.strip() for x in bairro.split(',')] if bairro else None,
        "ddd": [x.strip() for x in ddd.split(',')] if ddd else None,
        "nome_empresa": [x.strip() for x in nome_empresa.split(',')] if nome_empresa else None,
        "municipio": [x.strip() for x in municipio.split(',')] if municipio else None,
        "situacao_cadastral": [situacao_cadastral] if situacao_cadastral else None,
        "codigo_atividade_principal": [
            x.replace('-', '').replace('/', '') for x in codigo_atividade_principal.split(',') if x.strip()
        ] if codigo_atividade_principal else None,
        "data_abertura_inicio": data_abertura_inicio if data_abertura_inicio else None,
        "data_abertura_fim": data_abertura_fim if data_abertura_fim else None,
        "capital_social_minimo": capital_social_minimo if capital_social_minimo else None,
        "capital_social_maximo": capital_social_maximo if capital_social_maximo else None
    }

    # Botão para realizar a busca
    if st.button("Buscar"):
        # Fazer a requisição com os filtros
        resultados = fazer_requisicao(filtros)

        # Exibindo os resultados
        if "erro" in resultados:
            st.error(f"Erro na requisição: {resultados['erro']}")
        else:
            # Exibindo os resultados de forma mais bonita
            total = resultados['total']
            st.subheader(f"Total de resultados: {total}")
            
            # Criação da tabela para exibir os CNPJs
            cnpjs = resultados['cnpjs']
            df = pd.DataFrame(cnpjs)
            df['data'] = df['situacao_cadastral'].apply(lambda x: formatar_data(x['data'] if isinstance(x, dict) else None))
            df['situacao_atual'] = df['situacao_cadastral'].apply(lambda x: x['situacao_atual'] if isinstance(x, dict) else "N/A")
            df.drop(columns=['situacao_cadastral'], inplace=True)

            # Exibir a tabela formatada
            st.dataframe(df)

# Rodar a aplicação
if __name__ == "__main__":
    app()
