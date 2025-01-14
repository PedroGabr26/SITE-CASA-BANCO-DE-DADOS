import streamlit as st

# Título da aplicação
st.title("🏠 Site Casa dos Dados")

st.write("Bem-vindo à aplicação principal! Use o menu lateral para navegar entre as páginas.")
st.write("""
    Esse é um site experimental, no qual utilizamos a api da casa dos dados, e as funções mais importantes da mesma como: 
    - A busca por um cnpj, o qual você só pode fazer um por vez e ter acesso a variadas informações, desde o nome da empresa até o contato do lead, se o mesmo estiver no banco de dados da api.
    - E outra função é a busca avançada que por meio dos filtros você consegue econtrar varios CNPJs de uma só vez.
""")
st.write("A Casa dos Dados é uma plataforma onde voce encontra dados públicos de CNPJ (Cadastro Nacional de Pessoas Jurídicas) e consegue encontrar formas de identificar essa empresas pelos mais diversos filtros.")

st.subheader("📊 Objetivos do site")

st.write("""
Nosso objetivo é oferecer a você, empreendedor ou profissional, uma ferramenta poderosa para potencializar suas estratégias de negócios. 
Com a integração da API Casa dos Dados, você poderá:

- **Identificar oportunidades de mercado:** Encontre empresas relevantes para suas necessidades com base em filtros avançados como localização, setor de atuação, capital social, entre outros.
- **Facilitar a prospecção de clientes:** Acesse informações detalhadas e confiáveis de CNPJs, ajudando na tomada de decisão mais assertiva.
- **Economizar tempo e recursos:** Obtenha dados prontos para uso em poucos cliques, simplificando processos de pesquisa e análise.
- **Apoiar o crescimento do seu negócio:** Use as informações obtidas para planejar estratégias, estabelecer parcerias ou explorar novos segmentos de mercado.

Seja para expandir seu portfólio, construir relacionamentos comerciais ou realizar análises de mercado, o site está aqui para transformar dados em valor para o seu negócio!
""")

st.subheader("🔗 Mais Informações")
url = "https://portal.casadosdados.com.br/"
st.write("Plataforma Casa dos Dados : [link](%s)" % url)
api = "https://portal.casadosdados.com.br/docs/api"
st.write("Documentação API : [link](%s)" % api)
