from fastapi import FastAPI
from agents.observer_agent import observer_agent
from agents.report_agent import report_agent
from agents.chat_agent import chat_agent
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Scrum Master Backend is running"}

# to view  the brute data of the sprint
@app.get("/api/sprint-health")
def get_sprint_health():
    return {"data": observer_agent.get_sprint_health("SCRUM")}

# to generate the sprint report using AI
@app.get("/api/sprint-report")
def get_sprint_report():
    try:
        report = report_agent.generate_sprint_report("SCRUM")
        return {"report": report}
    except Exception as e:
        return {"error": str(e)}

# to handle chat messages
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat(request: ChatRequest):
    response = chat_agent.send_message(request.message)
    return {"reply": response}