from langchain.tools import tool
from langchain_community.utilities import GoogleSearchAPIWrapper
import requests
import os

# Ferramenta 1: Busca na Web (usando uma integração existente)
@tool
def web_search(query: str) -> str:
    """Útil para quando você precisa responder perguntas sobre eventos atuais ou pesquisar algo na internet."""
    search = GoogleSearchAPIWrapper()
    return search.run(query)

# Ferramenta 2: Escrever em um arquivo (uma ferramenta personalizada)
@tool
def write_file(filename: str, content: str) -> str:
    """Útil para escrever o conteúdo em um arquivo de texto."""
    # IMPORTANTE: Em produção, restrinja o acesso a um diretório seguro!
    # Por exemplo: safe_path = f"/path/to/user/sandboxes/{user_id}/{filename}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Arquivo '{filename}' escrito com sucesso."

# Ferramenta 3: Ler um arquivo
@tool
def read_file(filename: str) -> str:
    """Útil para ler o conteúdo de um arquivo de texto."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo '{filename}' não encontrado."

# Ferramenta 4: Pesquisa de receitas (original do seu código)
@tool
def search_recipes(query: str) -> str:
    """Pesquisa receitas em uma API externa com base em uma consulta."""
    api_key = os.getenv("RECIPE_API_KEY", "YOUR_RECIPE_API_KEY")
    base_url = os.getenv("RECIPE_API_BASE_URL", "https://api.edamam.com/api/recipes/v2")
    app_id = os.getenv("RECIPE_APP_ID", "YOUR_RECIPE_APP_ID")

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
        response.raise_for_status()
        data = response.json()
        if data and "hits" in data and len(data["hits"]) > 0:
            recipe = data["hits"][0]["recipe"]
            return "Receita encontrada: {} - {}".format(recipe["label"], recipe["url"])
        else:
            return f"Nenhuma receita encontrada para \'{query}\'"
    except requests.exceptions.RequestException as e:
        return f"Erro ao pesquisar receitas: {e}"

from .memory_manager import remember, learn

# Lista de ferramentas que o agente pode usar
available_tools = [
    web_search,
    write_file,
    read_file,
    search_recipes,
    remember,
    learn
]


