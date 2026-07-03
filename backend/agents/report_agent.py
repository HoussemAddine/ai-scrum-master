from typing import Optional

from agents.ai_client import get_llm
from agents.observer_agent import get_sprint_health

REPORT_PROMPT_TEMPLATE = """\
Tu es un Scrum Master expérimenté. Voici les données brutes de l'état du sprint
au format JSON :

{data}

Rédige un rapport court et actionnable pour l'équipe, en français, structuré ainsi :
1. **Résumé de l'avancement** (avancement réel vs attendu, en une phrase claire)
2. **Points de blocage** (liste les tickets bloqués s'il y en a, sinon dis qu'il n'y en a pas)
3. **Charge de l'équipe** (signale un déséquilibre s'il y en a un, sinon dis que la charge est équilibrée)
4. **Recommandation** (une ou deux actions concrètes pour le Scrum Master)

Reste concis : 150 mots maximum. N'invente aucune donnée qui n'est pas dans le JSON.
"""


def generate_report(project_key: str, board_id: Optional[int] = None) -> str:
    """
    Génère un rapport de sprint lisible à partir des données de santé du sprint.
    Combine l'outil d'observation (données factuelles Jira) avec le LLM
    (mise en forme et recommandations), plutôt que de renvoyer le JSON brut.
    """
    raw_result = get_sprint_health.invoke({"project_key": project_key, "board_id": board_id})

    llm = get_llm()
    prompt = REPORT_PROMPT_TEMPLATE.format(data=raw_result)
    response = llm.invoke(prompt)

    return response.content