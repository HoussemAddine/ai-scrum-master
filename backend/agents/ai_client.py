import os
from langchain_openai import ChatOpenAI

NARAROUTER_BASE_URL = "https://router.bynara.id/v1"


def get_llm():
    """
    Retourne une instance du LLM configurée pour passer par NaraRouter.
    Lève une erreur explicite si la clé API n'est pas configurée.
    """
    api_key = os.getenv("NARAROUTER_API_KEY") or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "NARAROUTER_API_KEY n'est pas définie. "
            "Ajoute-la dans ton fichier .env (clé au format sk-nry-...)."
        )

    model_alias = os.getenv("NARAROUTER_MODEL", "mistral-large")

    return ChatOpenAI(
        model=model_alias,
        api_key=api_key,
        base_url=NARAROUTER_BASE_URL,
        temperature=0,
    )