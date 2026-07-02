from agents.observer_agent import observer_agent
from agents.ai_client import get_ai_response

class ReportAgent:
    def generate_sprint_report(self, project_key="SCRUM"):
        # recuperr the data from the observer agent
        data = observer_agent.get_sprint_health(project_key)
        
        # the constructed prompt for the AI 
        prompt = f"""
        Tu es un expert Scrum Master. Analyse les données suivantes du sprint :
        {data}
        
        Produis un rapport court et motivant incluant :
        - Un résumé de l'avancement.
        - Une alerte si des tickets critiques sont en retard.
        - Une suggestion d'amélioration pour le prochain sprint.
        """
        
        # call the AI client to get the response
        return get_ai_response(prompt)

report_agent = ReportAgent()