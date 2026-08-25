from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
from datetime import datetime
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Session as DBSession, Message as DBMessage, ThreatModel
from threat_agent import create_threat_modeling_agent
from pdf_generator import generate_threat_report_pdf

app = FastAPI(title="ThreatModeler", description="AI-powered threat modeling platform")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    content: str
    framework: Optional[str] = None

class SessionCreate(BaseModel):
    framework: str  # STRIDE, PASTA, or HYBRID

class SessionResponse(BaseModel):
    id: int
    title: str
    framework: str
    created_at: datetime

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

# Initialize DB on startup
@app.on_event("startup")
async def startup():
    init_db()

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Get frameworks
@app.get("/api/frameworks")
async def get_frameworks():
    return {
        "frameworks": [
            {"id": "stride", "name": "STRIDE", "description": "Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege"},
            {"id": "pasta", "name": "PASTA", "description": "Process for Attack Simulation and Threat Analysis"},
            {"id": "phantom-b", "name": "PHANTOM-B", "description": "Probabilistic Heuristic Attack and Mitigation Model using Behavioral analysis"},
            {"id": "hybrid", "name": "Hybrid", "description": "Combined approach using STRIDE, PASTA, and PHANTOM-B frameworks"}
        ]
    }

# Create new session
@app.post("/api/sessions")
async def create_session(req: SessionCreate, db: Session = Depends(get_db)):
    session = DBSession(title=f"Threat Model - {datetime.now().strftime('%Y-%m-%d %H:%M')}", framework=req.framework)
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"id": session.id, "title": session.title, "framework": session.framework}

# Get session
@app.get("/api/sessions/{session_id}")
async def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"id": session.id, "title": session.title, "framework": session.framework, "created_at": session.created_at}

# Get session messages
@app.get("/api/sessions/{session_id}/messages")
async def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    messages = db.query(DBMessage).filter(DBMessage.session_id == session_id).all()
    return [{"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]

# Chat endpoint
@app.post("/api/sessions/{session_id}/chat")
async def chat(session_id: int, msg: ChatMessage, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Create agent for this session
    agent = create_threat_modeling_agent()

    # Load conversation history from DB
    messages = db.query(DBMessage).filter(DBMessage.session_id == session_id).all()
    for message in messages:
        agent.conversation_history.append({"role": message.role, "content": message.content})

    # Save user message
    user_msg = DBMessage(session_id=session_id, role="user", content=msg.content)
    db.add(user_msg)

    # Get AI response
    response = agent.chat(msg.content)

    # Save assistant message
    assistant_msg = DBMessage(session_id=session_id, role="assistant", content=response)
    db.add(assistant_msg)
    db.commit()

    return {"response": response}

# Generate report
@app.post("/api/sessions/{session_id}/generate-report")
async def generate_report(session_id: int, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all messages for this session
    messages = db.query(DBMessage).filter(DBMessage.session_id == session_id).all()
    if not messages:
        raise HTTPException(status_code=400, detail="No conversation found to generate report")

    # Create agent and recreate conversation
    agent = create_threat_modeling_agent()
    for msg in messages:
        agent.conversation_history.append({"role": msg.role, "content": msg.content})

    # Ask agent to generate final report
    final_prompt = "Based on our discussion, please provide the final threat modeling report in JSON format with all identified threats, data flows, and recommendations."
    report_response = agent.chat(final_prompt)

    # Parse threat report
    threat_report = agent.parse_threat_report(report_response)
    if not threat_report:
        threat_report = {
            "application_name": "Analyzed Application",
            "framework": session.framework,
            "summary": "Threat modeling analysis based on conversation",
            "threats": [],
            "data_flows": [],
            "recommendations": []
        }

    # Save threat model
    threat_model = ThreatModel(
        session_id=session_id,
        name=f"Threat Model - {session.title}",
        framework=session.framework,
        report_content=json.dumps(threat_report)
    )
    db.add(threat_model)
    db.commit()

    return threat_report

# Download report as PDF
@app.get("/api/sessions/{session_id}/download-pdf")
async def download_pdf(session_id: int, db: Session = Depends(get_db)):
    threat_model = db.query(ThreatModel).filter(ThreatModel.session_id == session_id).first()
    if not threat_model or not threat_model.report_content:
        raise HTTPException(status_code=404, detail="No report found")

    threat_data = json.loads(threat_model.report_content)
    pdf_bytes = generate_threat_report_pdf(threat_data)

    return FileResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        filename=f"threat_report_{session_id}.pdf"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
