from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import io
from datetime import datetime
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Session as DBSession, Message as DBMessage, ThreatModel
from threat_agent import create_threat_modeling_agent
from pdf_generator import generate_threat_report_pdf
from file_processor import process_uploaded_file, validate_file

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
    framework: Optional[str] = None  # Set later by user

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

# Update framework for session
@app.post("/api/sessions/{session_id}/framework")
async def update_framework(session_id: int, framework_data: dict, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    framework = framework_data.get("framework")
    session.framework = framework
    db.commit()
    return {"id": session.id, "framework": session.framework}

# Chat endpoint
@app.post("/api/sessions/{session_id}/chat")
async def chat(session_id: int, msg: ChatMessage, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Create agent with framework if set
    agent = create_threat_modeling_agent(framework=session.framework)

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

# Upload file endpoint
@app.post("/api/sessions/{session_id}/upload-file")
async def upload_file(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        # Read file content
        file_content = await file.read()

        # Validate file
        validate_file(file.filename, len(file_content))

        # Extract text from file
        extracted_text = await process_uploaded_file(file.filename, file_content)

        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text could be extracted from the file")

        # Send extracted text as a message
        user_message = f"I've uploaded a document ({file.filename}). Here's the content:\n\n{extracted_text}"

        # Create agent with current framework
        agent = create_threat_modeling_agent(framework=session.framework)

        # Load conversation history
        messages = db.query(DBMessage).filter(DBMessage.session_id == session_id).all()
        for message in messages:
            agent.conversation_history.append({"role": message.role, "content": message.content})

        # Save user message about the file
        user_msg = DBMessage(
            session_id=session_id,
            role="user",
            content=f"Uploaded document: {file.filename}"
        )
        db.add(user_msg)

        # Get AI response
        response = agent.chat(user_message)

        # Save assistant response
        assistant_msg = DBMessage(session_id=session_id, role="assistant", content=response)
        db.add(assistant_msg)
        db.commit()

        return {
            "filename": file.filename,
            "extracted_text_length": len(extracted_text),
            "response": response
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

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

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=threat_report_{session_id}.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
