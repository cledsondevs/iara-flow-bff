from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
import requests
import os

# Definir uma ferramenta para pesquisa de receitas em uma API externa
@tool
def search_recipes(query: str) -> str:
    """Pesquisa receitas em uma API externa com base em uma consulta."""
    # Exemplo de integração com uma API de receitas (substitua pela sua API real)
    # Para este exemplo, usaremos uma API de teste ou um mock
    # Você precisaria de uma chave de API real e uma URL base
    api_key = os.getenv("RECIPE_API_KEY", "YOUR_RECIPE_API_KEY")
    base_url = os.getenv("RECIPE_API_BASE_URL", "https://api.edamam.com/api/recipes/v2") # Exemplo
    app_id = os.getenv("RECIPE_APP_ID", "YOUR_RECIPE_APP_ID") # Exemplo

    if "YOUR_RECIPE_API_KEY" in api_key or "YOUR_RECIPE_APP_ID" in app_id:
        return f"Erro: Chave de API ou ID de aplicativo para receitas não configurados. Por favor, configure RECIPE_API_KEY e RECIPE_APP_ID no ambiente. Consulta: {query}"

    params = {
        "type": "public",
        "q": query,
        "app_id": app_id,
        "app_key": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Levanta um erro para status de erro HTTP
        data = response.json()
        if data and "hits" in data and len(data["hits"]) > 0:
            # Retorna o nome e URL da primeira receita encontrada
            recipe = data["hits"][0]["recipe"]
            return f"Receita encontrada: {recipe["label"]} - {recipe["url"]}"
        else:
            return f"Nenhuma receita encontrada para '{query}'."
    except requests.exceptions.RequestException as e:
        return f"Erro ao pesquisar receitas: {e}"

# Lista de ferramentas que o agente pode usar
tools = [
    search_recipes,
]

# Modelo de linguagem para o agente
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Prompt para o agente ReAct
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente útil que pode pesquisar receitas. Use a ferramenta 'search_recipes' se o usuário pedir uma receita ou informações sobre culinária."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Criar o agente ReAct
agent = create_react_agent(llm, tools, prompt)

# Criar o executor do agente
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Função para invocar o agente
def invoke_langchain_agent(query: str) -> str:
    try:
        response = agent_executor.invoke({"input": query})
        return response["output"]
    except Exception as e:
        return f"Erro ao invocar o agente LangChain: {e}"


