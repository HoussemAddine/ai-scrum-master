import json
from typing import Optional

from langchain_core.tools import tool
from jira_service import jira_service


@tool
def get_sprint_health(project_key: str, board_id: Optional[int] = None) -> str:
    """
    Récupère l'état de santé du sprint actif pour un projet Jira donné :
    avancement réel vs attendu, tickets bloqués, et déséquilibre de charge
    entre les membres de l'équipe.

    Args:
        project_key: la clé du projet Jira (ex: "SCRUM").
        board_id: optionnel, l'id du board Jira pour calculer l'avancement
                  attendu basé sur les dates du sprint. Sans lui, seul
                  l'avancement réel (tickets Done / total) est calculé.
    """
    try:
        data = jira_service.get_sprint_health(project_key, board_id=board_id)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)