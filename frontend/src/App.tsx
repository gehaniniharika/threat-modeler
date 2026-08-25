import { useEffect, useState } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'

function App() {
  const [sessionId, setSessionId] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await fetch('/api/sessions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ framework: null })
        })
        const data = await response.json()
        setSessionId(data.id)
      } catch (err) {
        setError('Failed to create session')
      } finally {
        setLoading(false)
      }
    }

    initSession()
  }, [])

  if (loading) {
    return <div className="app loading"><p>Loading application...</p></div>
  }

  if (error) {
    return <div className="app"><div className="error-banner">{error}</div></div>
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛡️ ThreatModeler</h1>
        <p>AI-powered threat modeling for web applications</p>
      </header>

      <main className="app-main">
        {sessionId && <ChatInterface sessionId={sessionId} />}
      </main>
    </div>
  )
}

export default App
