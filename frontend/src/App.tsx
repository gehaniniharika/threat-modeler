import { useEffect, useState } from 'react'
import './App.css'

interface Framework {
  id: string
  name: string
  description: string
}

function App() {
  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFrameworks = async () => {
      try {
        const response = await fetch('/api/frameworks')
        if (!response.ok) throw new Error('Failed to fetch frameworks')
        const data = await response.json()
        setFrameworks(data.frameworks)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchFrameworks()
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛡️ ThreatModeler</h1>
        <p>AI-powered threat modeling for web applications</p>
      </header>

      <main className="app-main">
        <section className="intro">
          <h2>Welcome to ThreatModeler</h2>
          <p>Analyze your application architecture for security threats using industry-standard frameworks.</p>
        </section>

        <section className="frameworks">
          <h2>Available Frameworks</h2>
          {loading && <p>Loading frameworks...</p>}
          {error && <p className="error">Error: {error}</p>}
          {!loading && !error && (
            <div className="framework-grid">
              {frameworks.map((fw) => (
                <div key={fw.id} className="framework-card">
                  <h3>{fw.name}</h3>
                  <p>{fw.description}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="get-started">
          <h2>Get Started</h2>
          <div className="steps">
            <div className="step">
              <span className="step-number">1</span>
              <p>Upload your design documents (PDF, Word docs)</p>
            </div>
            <div className="step">
              <span className="step-number">2</span>
              <p>Connect your GitHub repository or upload Figma diagrams</p>
            </div>
            <div className="step">
              <span className="step-number">3</span>
              <p>Select your threat modeling framework</p>
            </div>
            <div className="step">
              <span className="step-number">4</span>
              <p>Review generated DFD diagrams and threat reports</p>
            </div>
          </div>
          <button className="cta-button">Start Threat Modeling</button>
        </section>
      </main>
    </div>
  )
}

export default App
