from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain.memory import ConversationBufferWindowMemory
from .tools import available_tools

llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)

prompt = hub.pull("hwchase17/openai-functions-agent")

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=10,
    return_messages=True
)

agent = create_openai_tools_agent(llm, available_tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=available_tools,
    memory=memory,
    verbose=True,
    max_iterations=15,
    handle_parsing_errors=True
)

def invoke_langchain_agent(query: str, user_id: str) -> str:
    try:
        response = agent_executor.invoke({"input": query, "user_id": user_id})
        return response["output"]
    except Exception as e:
        return f"Erro ao invocar o agente LangChain: {e}"


