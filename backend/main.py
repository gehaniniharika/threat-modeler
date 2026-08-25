from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="ThreatModeler", description="AI-powered threat modeling platform")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Example endpoint
@app.get("/api/frameworks")
async def get_frameworks():
    return {
        "frameworks": [
            {"id": "stride", "name": "STRIDE", "description": "Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege"},
            {"id": "pasta", "name": "PASTA", "description": "Process for Attack Simulation and Threat Analysis"},
            {"id": "any", "name": "Generic", "description": "Hybrid approach combining multiple frameworks"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
