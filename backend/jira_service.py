import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

class JiraService:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
        )

    def get_sprint_tickets(self, project_key):
        """Récupère les tickets du projet et les formate pour l'IA."""
        # On récupère les tickets (ici un JQL simple, on pourra l'affiner)
        issues = self.jira.search_issues(f'project="{project_key}"')
        
        formatted_tickets = []
        for issue in issues:
            formatted_tickets.append({
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "priority": issue.fields.priority.name if issue.fields.priority else "None",
                "description": issue.fields.description
            })
        return formatted_tickets

# Instance unique à importer dans main.py
jira_service = JiraService()