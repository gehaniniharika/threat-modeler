# ThreatModeler - Project Context

## Project Overview
ThreatModeler is an AI-powered threat modeling platform that helps developers and security teams identify security threats in web applications using industry-standard frameworks.

### Core Purpose
Automate threat identification by analyzing:
- Design documents (PDFs, Word docs)
- GitHub source code repositories
- Figma architecture diagrams

And output:
- Data Flow Diagrams (DFD)
- Threat reports with severity ratings
- Mitigation recommendations

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **File Processing**: PyPDF2, python-docx, requests (for GitHub)
- **Server**: Uvicorn
- **Port**: 8000

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Port**: 5173
- **Styling**: Plain CSS (no CSS-in-JS library)

### Architecture
- **Monorepo structure**: `backend/` and `frontend/` directories
- **API Pattern**: RESTful with CORS enabled for frontend dev
- **Database**: Local SQLite (can migrate to PostgreSQL)

## Key Features

### Threat Modeling Frameworks
Users can choose:
1. **STRIDE** - Microsoft's threat modeling approach
   - Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
2. **PASTA** - Process for Attack Simulation and Threat Analysis
3. **Generic** - Hybrid approach combining multiple frameworks

### Main Workflows
1. User uploads design documents and source code
2. Selects threat modeling framework
3. System analyzes and generates DFD diagrams
4. System identifies threats and generates report
5. User reviews risks and mitigations

## Database Schema

### ThreatModel (Projects)
- Stores threat modeling projects
- Links to threats and data flows
- Tracks framework selection

### Threat (Findings)
- Individual threats identified
- Severity levels: Critical, High, Medium, Low
- Maps to framework categories (STRIDE/PASTA)
- Includes mitigation suggestions

### DataFlow (Architecture)
- Data flows between components
- Protocol and data type information
- Used for DFD visualization

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Both Servers
Start in separate terminals to run full stack with API proxy at `/api`

## Current State

### Implemented
- ✅ Project structure
- ✅ FastAPI boilerplate with health check
- ✅ Database models and SQLAlchemy setup
- ✅ React + Vite setup with TypeScript
- ✅ Basic landing page with framework overview
- ✅ API proxy configuration in Vite

### Not Yet Implemented
- Document parsing (PDF/Word analysis)
- GitHub repository integration
- Threat modeling logic (STRIDE/PASTA algorithms)
- DFD visualization component
- Report generation
- User authentication
- Project management UI
- Figma integration

## Important Notes

### Security Considerations
- Add GitHub token validation in production
- Implement authentication before deployment
- Sanitize uploaded files
- Validate all user inputs

### Database
- Currently SQLite for development
- Can be migrated to PostgreSQL by changing DATABASE_URL
- Use SQLAlchemy's async support for better performance

### API Design
- Prefix all routes with `/api/`
- Use proper HTTP status codes
- Consistent error response format
- CORS configured for localhost development

## Future Enhancements

1. **AI Integration**: Use Claude API to help analyze threats
2. **Real-time Collaboration**: WebSocket support for collaborative analysis
3. **DFD Editor**: Visual DFD creation and editing
4. **Automated Scoring**: Risk scoring based on threat severity
5. **Integration**: JIRA, GitHub Issues for threat tracking
6. **Export**: PDF reports, JSON data export

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: SQLite connection string (default: sqlite:///./threat_modeler.db)
- `DEBUG`: Enable debug mode (default: True)
- `GITHUB_TOKEN`: GitHub API token for repo access

## File Upload Locations
- Uploads stored in `backend/uploads/` directory
- Temporary processing in `backend/temp/`
- Configure before production deployment

## Testing
- Backend: pytest framework (to be added)
- Frontend: Vitest + React Testing Library (to be added)
