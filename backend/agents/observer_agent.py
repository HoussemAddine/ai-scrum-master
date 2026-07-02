from jira_service import jira_service

class ObserverAgent:
    def __init__(self):
        self.service = jira_service

    def get_sprint_health(self, project_key="SCRUM"):
        """Analyse l'état des tickets et retourne un résumé structuré."""
        tickets = self.service.get_sprint_tickets(project_key)
        
        # categorization of tickets to facilitate the analysis for the AI
        health = {
            "total": len(tickets),
            "done": [t for t in tickets if t['status'] == "Done"],
            "in_progress": [t for t in tickets if t['status'] == "In Progress"],
            "to_do": [t for t in tickets if t['status'] == "To Do"],
        }
        return health

# On crée une instance pour l'utiliser facilement
observer_agent = ObserverAgent()