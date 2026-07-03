try:
    from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate
from agents.ai_client import get_llm
from agents.observer_agent import get_sprint_health


class ChatAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [get_sprint_health]

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Tu es un Scrum Master expert. Utilise les outils fournis pour "
                "répondre aux questions sur l'état du sprint Jira. Si un outil "
                "renvoie une erreur, explique-la clairement à l'utilisateur "
                "plutôt que d'inventer une réponse.",
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        )

    def send_message(self, message: str) -> str:
        result = self.agent_executor.invoke({"input": message})
        return result["output"]