import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

def get_jira_client():
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")
    return JIRA(server=jira_url, basic_auth=(jira_email, jira_token))

def create_advanced_mock_tickets(jira, project_key="SCRUM"):
    # Liste des tickets avec leur état cible
    mock_data = [
        {"summary": "Setup Project Repo", "status": "Done", "description": "Initialize Git repository"},
        {"summary": "Design Database Schema", "status": "Done", "description": "Create ERD diagram"},
        {"summary": "Implement Auth API", "status": "In Progress", "description": "Integrate JWT authentication"},
        {"summary": "Create Frontend Login Page", "status": "In Progress", "description": "Form validation and styling"},
        {"summary": "Write Unit Tests", "status": "To Do", "description": "Cover API endpoints with pytest"},
        {"summary": "Deploy to Staging", "status": "To Do", "description": "Configure CI/CD pipeline"},
    ]

    for item in mock_data:
        # 1. Création du ticket
        issue_dict = {
            'project': {'key': project_key},
            'summary': item['summary'],
            'description': item['description'],
            'issuetype': {'name': 'Task'},
        }
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Créé: {new_issue.key} [{item['status']}]")

        # 2. Transition vers l'état demandé
        # Note : Les noms de transition (ex: 'Done', 'In Progress') dépendent de ta configuration Jira
        if item['status'] != "To Do":
            try:
                # Jira Cloud utilise les noms de transition pour passer d'un état à l'autre
                jira.transition_issue(new_issue, transition=item['status'])
                print(f" -> Transition vers {item['status']} effectuée.")
            except Exception as e:
                print(f" -> Attention : Impossible de passer en {item['status']} (Vérifie le nom de la transition). Erreur: {e}")

if __name__ == "__main__":
    client = get_jira_client()
    create_advanced_mock_tickets(client)