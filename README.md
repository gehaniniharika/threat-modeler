# ThreatModeler

AI-powered threat modeling platform for web applications. Analyze your application architecture for security threats using industry-standard frameworks (STRIDE, PASTA).

## Features

- **Multiple Frameworks**: Support for STRIDE, PASTA, and hybrid approaches
- **Document Analysis**: Upload design documents (PDF, Word) for automatic analysis
- **Code Integration**: Connect GitHub repositories for codebase analysis
- **Diagram Support**: Upload or integrate Figma diagrams
- **DFD Generation**: Automatically generate Data Flow Diagrams
- **Threat Reports**: Comprehensive threat modeling reports with severity ratings and mitigations

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite
- **File Processing**: PyPDF2, python-docx
- **API**: RESTful with CORS support

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: CSS3
- **HTTP Client**: Axios (configured for API proxy)

## Project Structure

```
threat-modeler/
├── backend/                 # FastAPI application
│   ├── main.py             # Main application entry point
│   ├── database.py         # SQLAlchemy configuration
│   ├── models.py           # Database models
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # React application
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # App styles
│   │   ├── main.tsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite configuration
│   └── tsconfig.json       # TypeScript configuration
└── README.md               # This file
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Create a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Initialize the database:
```bash
python -c "from database import init_db; init_db()"
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Development

### Running Both Servers

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## API Endpoints

### Available Endpoints

- `GET /api/health` - Health check
- `GET /api/frameworks` - Get available threat modeling frameworks

More endpoints coming soon:
- `POST /api/analysis/upload` - Upload design documents
- `POST /api/analysis/github` - Analyze GitHub repository
- `POST /api/analysis/generate-dfd` - Generate DFD diagrams
- `GET /api/analysis/:id/threats` - Get identified threats
- `GET /api/analysis/:id/report` - Get threat modeling report

## Database Models

### ThreatModel
- id: Primary key
- name: Project name
- description: Project description
- framework: STRIDE, PASTA, or ANY
- created_at, updated_at: Timestamps

### Threat
- id: Primary key
- model_id: Reference to ThreatModel
- title: Threat title
- description: Detailed description
- severity: Critical, High, Medium, Low
- category: STRIDE or PASTA category
- mitigation: Suggested mitigation
- created_at: Timestamp

### DataFlow
- id: Primary key
- model_id: Reference to ThreatModel
- source: Source component
- destination: Destination component
- data_type: Type of data flowing
- protocol: Communication protocol
- created_at: Timestamp

## Next Steps

1. Implement document parsing (PDF/Word)
2. Build GitHub integration
3. Create DFD visualization component
4. Implement STRIDE and PASTA threat modeling logic
5. Build report generation
6. Add user authentication
7. Create project management features

## Contributing

1. Create a feature branch
2. Make your changes
3. Test both backend and frontend
4. Submit a pull request

## License

MIT License - See LICENSE file for details
