import os
from google import genai
from agents.observer_agent import observer_agent

class ChatAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.initialized = False  # Track if context is sent

    def _initialize_context(self):
        """Lazy initialization of the context."""
        if not self.initialized:
            try:
                sprint_data = observer_agent.get_sprint_health("SCRUM")
                context_prompt = (
                    f"You are an expert AI Scrum Master. "
                    f"Current sprint status: {sprint_data}. "
                    "Always answer in French."
                )
                self.chat.send_message(context_prompt)
                self.initialized = True
            except Exception as e:
                print(f"Context initialization failed: {e}")

    def send_message(self, message: str):
        # Initialize context on the first message
        self._initialize_context()
        
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return "Désolé, l'IA est temporairement indisponible (serveurs saturés). Réessaie dans un instant."

chat_agent = ChatAgent()