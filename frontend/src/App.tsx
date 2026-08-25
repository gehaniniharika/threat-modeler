import { useEffect, useState } from 'react'
import './App.css'
import FrameworkSelector from './components/FrameworkSelector'
import ChatInterface from './components/ChatInterface'

interface Framework {
  id: string
  name: string
  description: string
}

type AppState = 'selecting-framework' | 'chatting'

function App() {
  const [state, setState] = useState<AppState>('selecting-framework')
  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [selectedFramework, setSelectedFramework] = useState<string>('')
  const [sessionId, setSessionId] = useState<number | null>(null)
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

  const handleFrameworkSelect = async (frameworkId: string) => {
    setSelectedFramework(frameworkId)
    try {
      const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ framework: frameworkId })
      })
      const data = await response.json()
      setSessionId(data.id)
      setState('chatting')
    } catch (err) {
      setError('Failed to create session')
    }
  }

  const handleBackToFrameworks = () => {
    setState('selecting-framework')
    setSessionId(null)
    setSelectedFramework('')
  }

  if (loading) {
    return <div className="app loading"><p>Loading application...</p></div>
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛡️ ThreatModeler</h1>
        <p>AI-powered threat modeling for web applications</p>
      </header>

      <main className="app-main">
        {error && <div className="error-banner">{error}</div>}

        {state === 'selecting-framework' && (
          <FrameworkSelector
            frameworks={frameworks}
            onSelect={handleFrameworkSelect}
          />
        )}

        {state === 'chatting' && sessionId && (
          <ChatInterface
            sessionId={sessionId}
            framework={selectedFramework}
            onBack={handleBackToFrameworks}
          />
        )}
      </main>
    </div>
  )
}

export default App
