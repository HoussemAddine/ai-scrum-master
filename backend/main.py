import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.chat_agent import ChatAgent
from agents.report_agent import generate_report
from jira_service import jira_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scrum_master_ai")

app = FastAPI(title="Scrum Master AI Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


chat_agent: Optional[ChatAgent] = None


@app.on_event("startup")
def startup_event():
    global chat_agent
    try:
        chat_agent = ChatAgent()
        logger.info("ChatAgent initialisé avec succès.")
    except Exception as e:
        logger.error(f"Échec de l'initialisation du ChatAgent : {e}")
        chat_agent = None


class ChatRequest(BaseModel):
    message: str


class ReportRequest(BaseModel):
    project_key: str
    board_id: Optional[int] = None


@app.get("/")
def read_root():
    return {"status": "online", "message": "Scrum Master AI Backend est prêt."}


@app.get("/health")
def health_check():
    """Vérifie l'état des dépendances externes sans faire planter l'app si elles sont down."""
    return {
        "api": "ok",
        "chat_agent": "ok" if chat_agent is not None else "unavailable",
        "jira": "ok" if jira_service.is_connected() else "unavailable",
    }


@app.post("/api/chat")
def ask_ai(request: ChatRequest):

    if chat_agent is None:
        raise HTTPException(
            status_code=503,
            detail="L'agent de chat n'est pas disponible (voir /health pour le diagnostic).",
        )

    try:
        response = chat_agent.send_message(request.message)
        return {"response": response}
    except Exception as e:
        logger.exception("Erreur lors du traitement du message de chat.")
        raise HTTPException(status_code=500, detail="Erreur interne lors du traitement du message.")


@app.post("/api/report")
def get_report(request: ReportRequest):
    try:
        report = generate_report(request.project_key, board_id=request.board_id)
        return {"report": report}
    except Exception as e:
        logger.exception("Erreur lors de la génération du rapport.")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la génération du rapport.")