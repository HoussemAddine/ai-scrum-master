import os
from collections import defaultdict
from datetime import datetime, timezone

from jira import JIRA
from dotenv import load_dotenv

load_dotenv()


BLOCKED_KEYWORDS = ["block", "bloqu", "impediment", "on hold", "en attente"]


class JiraService:

    def __init__(self):
        self._jira = None

    @property
    def jira(self) -> JIRA:
        if self._jira is None:
            server = os.getenv("JIRA_URL")
            email = os.getenv("JIRA_EMAIL")
            token = os.getenv("JIRA_API_TOKEN")

            if not all([server, email, token]):
                raise RuntimeError(
                    "Configuration Jira incomplète. Vérifie JIRA_URL, JIRA_EMAIL "
                    "et JIRA_API_TOKEN dans ton .env."
                )

            self._jira = JIRA(server=server, basic_auth=(email, token))
        return self._jira

    def is_connected(self) -> bool:
        """Permet à /health de vérifier la connexion sans planter l'app."""
        try:
            self.jira.myself()
            return True
        except Exception:
            return False


    def get_sprint_tickets(self, project_key: str, sprint_only: bool = True):
        """
        Récupère les tickets du projet et les formate pour l'IA.
        Si sprint_only=True, se limite aux tickets du sprint actif (JQL 'openSprints()').
        """
        jql = f'project = "{project_key}"'
        if sprint_only:
            jql += " AND sprint in openSprints()"

        issues = self.jira.search_issues(jql, maxResults=200)

        formatted_tickets = []
        for issue in issues:
            fields = issue.fields
            formatted_tickets.append({
                "key": issue.key,
                "summary": fields.summary,
                "status": fields.status.name,
                "status_category": fields.status.statusCategory.name,
                "priority": fields.priority.name if fields.priority else "None",
                "assignee": fields.assignee.displayName if fields.assignee else "Non assigné",
                "description": fields.description,
                "flagged": self._is_blocked(fields),
            })
        return formatted_tickets

    def _is_blocked(self, fields) -> bool:
        """
        Détecte un ticket bloqué :
        1. Champ Jira natif 'Flagged' (customfield_10021 sur beaucoup d'instances Cloud).
        2. Fallback : mots-clés dans le nom du statut.
        """
        flagged_field = getattr(fields, "customfield_10021", None)
        if flagged_field:
            return True

        status_name = fields.status.name.lower()
        return any(keyword in status_name for keyword in BLOCKED_KEYWORDS)


    def get_active_sprint_window(self, board_id: int):
        """Retourne (start_date, end_date, sprint_name) du sprint actif d'un board, ou None."""
        sprints = self.jira.sprints(board_id, state="active")
        if not sprints:
            return None
        sprint = sprints[0]
        return {
            "name": sprint.name,
            "start": getattr(sprint, "startDate", None),
            "end": getattr(sprint, "endDate", None),
        }

    def get_sprint_health(self, project_key: str, board_id: int | None = None):

        tickets = self.get_sprint_tickets(project_key, sprint_only=True)

        total = len(tickets)
        by_category = defaultdict(int)
        blocked_tickets = []
        load_per_assignee = defaultdict(int)

        for t in tickets:
            by_category[t["status_category"]] += 1
            load_per_assignee[t["assignee"]] += 1
            if t["flagged"]:
                blocked_tickets.append({"key": t["key"], "summary": t["summary"]})

        done = by_category.get("Done", 0)
        in_progress = by_category.get("In Progress", 0)
        todo = by_category.get("To Do", 0)

        actual_progress_pct = round((done / total) * 100, 1) if total else 0.0

        # Avancement attendu basé sur le temps écoulé du sprint (si dates disponibles)
        expected_progress_pct = None
        sprint_window = None
        if board_id:
            try:
                sprint_window = self.get_active_sprint_window(board_id)
            except Exception:
                sprint_window = None

        if sprint_window and sprint_window["start"] and sprint_window["end"]:
            start = datetime.fromisoformat(sprint_window["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(sprint_window["end"].replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            total_duration = (end - start).total_seconds()
            elapsed = (now - start).total_seconds()
            if total_duration > 0:
                time_ratio = max(0.0, min(1.0, elapsed / total_duration))
                expected_progress_pct = round(time_ratio * 100, 1)

        # Déséquilibre de charge : écart entre la charge max et la charge moyenne
        load_values = list(load_per_assignee.values())
        avg_load = round(sum(load_values) / len(load_values), 1) if load_values else 0
        max_load = max(load_values) if load_values else 0
        load_imbalance_detected = bool(load_values) and (max_load - avg_load) >= max(2, avg_load * 0.5)

        return {
            "project_key": project_key,
            "sprint_name": sprint_window["name"] if sprint_window else None,
            "total_tickets": total,
            "done": done,
            "in_progress": in_progress,
            "todo": todo,
            "actual_progress_pct": actual_progress_pct,
            "expected_progress_pct": expected_progress_pct,
            "progress_gap_pct": (
                round(actual_progress_pct - expected_progress_pct, 1)
                if expected_progress_pct is not None else None
            ),
            "blocked_tickets": blocked_tickets,
            "blocked_count": len(blocked_tickets),
            "load_per_assignee": dict(load_per_assignee),
            "load_imbalance_detected": load_imbalance_detected,
        }



jira_service = JiraService()