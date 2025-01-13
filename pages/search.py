import streamlit as st
import requests
import pandas as pd

st.title("Página 2")

#st.subheader("🔑 Coloque sua API Key")
st.title("🔍 Consulta de CNPJ - Casa dos Dados")
st.subheader("Bem-vindo! Realize buscas detalhadas de CNPJs com informações ricas e organizadas.")
#st.write("Bem-vindo! Realize buscas detalhadas de CNPJs com informações ricas e organizadas.")
st.write("🔑 Coloque sua API Key")

api_key = st.text_input("",type='password')

#if api_key:
#    st.session_state["api-key"] = api_key
#    st.success("Chave salva com sucesso")

if api_key.strip():
    st.subheader("Busque já o seu próximo LEAD 👇")
    cnpj = st.text_input("Digite seu cnpj ", key='cnpj_input')
    if st.button("🔍 Buscar CNPJ"):
        url = f"https://api.casadosdados.com.br/v4/cnpj/{cnpj}"
        headers = {
        "api-key":f"{api_key}"
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "cnpj" in data: # OU if data:
                # Exibe as informações de forma organizada
                st.success("✅ Consulta realizada com sucesso!")
                st.write("---")
                st.subheader("📊 Informações Gerais")
                st.write(f"**Razão Social**: {data['razao_social']}")
                st.write(f"**CNPJ**: {data['cnpj']}")
                st.write(f"**CNPJ Raiz**: {data['cnpj_raiz']}")
                st.write(f"**Matriz ou Filial**: {data['matri_filial']}")
                st.write(f"**Natureza Jurídica**: {data['descricao_natureza_juridica']}")
                st.write(f"**Qualificação do Responsável**: {data['qualificacao_responsavel']['descricao']}")
                st.write(f"**Porte da Empresa**: {data['porte_empresa']['descricao']}")
                st.write(f"**Situação Cadastral**: {data['situacao_cadastral']['situacao_atual']}")
                st.write(f"**Motivo da Situação Cadastral**: {data['situacao_cadastral']['motivo']}")
                st.write(f"**Data da Situação Cadastral**: {data['situacao_cadastral']['data']}")

                # Exibe o endereço
                st.subheader("📍 Endereço")
                st.write("**Endereço**:")
                st.write(f"**Logradouro**: {data['endereco']['logradouro']}, {data['endereco']['numero']}")
                st.write(f"**Bairro**: {data['endereco']['bairro']}")
                st.write(f"**Cidade**: {data['endereco']['municipio']}")
                st.write(f"**Estado**: {data['endereco']['uf']}")
                st.write(f"**CEP**: {data['endereco']['cep']}")

                # Exibe as atividades econômicas
                st.subheader("💼 Atividades Econômicas")
                st.write(f"**Atividade Principal**: {data['atividade_principal']['descricao']}")
                st.write("**Atividades Secundárias**:")
                for atividade in data['atividade_secundaria']:
                    st.write(f"{atividade['codigo']} - {atividade['descricao']}")

                # Exibe informações do IBGE
                st.subheader("📊 Informações do IBGE")
                st.write(f"**Código Município**: {data['endereco']['ibge']['codigo_municipio']}")
                st.write(f"**Código UF**: {data['endereco']['ibge']['codigo_uf']}")
                st.write(f"**Latitude**: {data['endereco']['ibge']['latitude']}")
                st.write(f"**Longitude**: {data['endereco']['ibge']['longitude']}")

                st.subheader("📅 Dados Cadastrais")
                st.write(f"**Data de abertura **:{data['data_abertura']}")
                st.write(f"**Capital Social**: R$ {data['capital_social']:,.2f}")

                # Exibe informações sobre o MEI (Microempreendedor Individual)

                st.write("**Informações sobre o MEI**:")
                if data['mei']['optante']:
                    st.write(f"Optante pelo MEI desde: {data['mei']['data_opcao_mei']}")
                else:
                    st.write("Não é optante pelo MEI.")

                # Exibe informações sobre o Simples Nacional
                st.subheader("🟢 Simples Nacional")
                st.write("**Informações sobre o Simples Nacional**:")
                if data['simples']['optante']:
                    st.write(f"Optante pelo Simples Nacional desde: {data['simples']['data_opcao_simples']}")
                else:
                    st.write("Não é optante pelo Simples Nacional.")

                # Exibe os contatos telefônicos
                st.subheader("📞 Contatos")
                st.write("**Contatos Telefônicos**:")
                for contato in data['contato_telefonico']:
                    st.write(f"- {contato['completo']} (Tipo: {contato['tipo']})")

                # Exibe contatos de email (caso existam)

                if data['contato_email']:
                    st.write("**Emails de Contato**:")
                    for email in data['contato_email']:
                        st.write(f"- {email}")
                else:
                    st.write("**Emails de Contato**: Nenhum email disponível.")
        else:
            st.error("❌ CNPJ não encontrado ou inválido.")
            st.error(f"❌ ERROR:{response.status_code}")
else:
    st.info("⚠️ Insira sua API Key para habilitar a consulta.")


# colocar uma lupa do lado da barra de pesquisa - NÃO ALINHA
# mudar a visualização de como recebemos os parametros do cnpj - FEITO
# OBS: procurei como usava a nossa requisição no streamlit, como criava a area pra pôr o cnpj, e assim consecutivamente descobri como utilizar corretamente o valor desse cnpj na url, eu sabia como fazer, só não sabia qual variável usar
# OBS: quando trabalhamos com 2 text_input precisamos de uma key pra cada um deles eu consegui fazer sozinho a lógica de pedir a chave api, mas precisava da lógica da key de cada um (tive uma mãozinha)
# OBS: pedi pro chat ajudar na estilização do meu site