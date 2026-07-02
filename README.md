
# AI Scrum Master

A tool to automate Scrum project management using the Jira Cloud API.

## Prerequisites

* Docker & Docker Compose
* Python 3.11+

## Configuration

1. Create a `.env` file at the root of the project:
```text
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

```

## Usage

### Run the project

```bash
docker compose up -d --build

```

### Stop the project

```bash
docker compose down

```

### Backend development (Local)

To install dependencies or run scripts manually from the root:

```bash
# Setup virtual environment
python -m venv backend/venv
source backend/venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

```

## Services

* **Backend API**: `http://localhost:8000`
* **Frontend App**: `http://localhost:5173`

---