import { useEffect, useRef, useState } from 'react'
import './ChatInterface.css'
import FrameworkSelector from './FrameworkSelector'

interface Message {
  id: number
  role: string
  content: string
  created_at: string
}

interface Framework {
  id: string
  name: string
  description: string
}

interface Props {
  sessionId: number
}

export default function ChatInterface({ sessionId }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null)
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [reportReady, setReportReady] = useState(false)
  const [showFrameworkSelector, setShowFrameworkSelector] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load conversation history and frameworks on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [messagesRes, frameworksRes] = await Promise.all([
          fetch(`/api/sessions/${sessionId}/messages`),
          fetch('/api/frameworks')
        ])

        const messagesData = await messagesRes.json()
        const frameworksData = await frameworksRes.json()

        setMessages(messagesData)
        setFrameworks(frameworksData.frameworks)

        // If no messages, send initial greeting
        if (messagesData.length === 0) {
          sendInitialGreeting()
        }

        scrollToBottom()
      } catch (err) {
        console.error('Failed to load data:', err)
      }
    }

    loadData()
  }, [sessionId])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendInitialGreeting = async () => {
    const greeting = "Please help me with threat modeling. I want to analyze my web application for security threats."
    await sendMessage(greeting)
  }

  const sendMessage = async (content: string) => {
    if (!content.trim()) return

    setLoading(true)
    try {
      const response = await fetch(`/api/sessions/${sessionId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
      })

      if (!response.ok) throw new Error('Failed to send message')

      // Reload messages to get the latest
      const messagesResponse = await fetch(`/api/sessions/${sessionId}/messages`)
      const newMessages = await messagesResponse.json()
      setMessages(newMessages)
      setInputValue('')

      // Show framework selector after 4+ exchanges
      if (newMessages.length >= 4 && !selectedFramework && !showFrameworkSelector) {
        setShowFrameworkSelector(true)
      }
    } catch (err) {
      console.error('Failed to send message:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(inputValue)
  }

  const handleFrameworkSelect = async (frameworkId: string) => {
    setSelectedFramework(frameworkId)
    setShowFrameworkSelector(false)

    try {
      await fetch(`/api/sessions/${sessionId}/framework`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ framework: frameworkId })
      })

      // Send confirmation message
      const frameworkName = frameworks.find(f => f.id === frameworkId)?.name || frameworkId
      await sendMessage(`Great! I'll analyze your application using the ${frameworkName} threat modeling framework. Based on what you've shared, let me identify the key threats and vulnerabilities...`)
    } catch (err) {
      console.error('Failed to set framework:', err)
    }
  }

  const handleGenerateReport = async () => {
    if (!selectedFramework) {
      alert('Please select a threat modeling framework first')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`/api/sessions/${sessionId}/generate-report`, {
        method: 'POST'
      })

      if (response.ok) {
        setReportReady(true)
      }
    } catch (err) {
      console.error('Failed to generate report:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch(`/api/sessions/${sessionId}/download-pdf`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `threat_report_${sessionId}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Failed to download PDF:', err)
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-title">
          <h2>Threat Modeling Chat</h2>
          {selectedFramework && (
            <p>Framework: <strong>{frameworks.find(f => f.id === selectedFramework)?.name || selectedFramework.toUpperCase()}</strong></p>
          )}
        </div>
        <div className="chat-actions">
          {reportReady && (
            <button className="download-btn" onClick={handleDownloadPDF}>
              📄 Download PDF Report
            </button>
          )}
          {selectedFramework && !reportReady && messages.length > 4 && (
            <button className="generate-btn" onClick={handleGenerateReport} disabled={loading}>
              {loading ? 'Generating...' : '✓ Generate Report'}
            </button>
          )}
        </div>
      </div>

      <div className="messages-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.role === 'user' ? '👤' : '🤖'} {msg.content}
            </div>
          </div>
        ))}

        {showFrameworkSelector && (
          <div className="framework-selector-overlay">
            <FrameworkSelector
              frameworks={frameworks}
              onSelect={handleFrameworkSelect}
            />
          </div>
        )}

        {loading && (
          <div className="message assistant">
            <div className="message-content typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedFramework ? "Ask follow-up questions or provide more details..." : "Describe your application architecture..."}
          disabled={loading || showFrameworkSelector}
          className="chat-input"
        />
        <button type="submit" disabled={loading || showFrameworkSelector} className="send-button">
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  )
}
