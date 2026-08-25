import { useEffect, useRef, useState } from 'react'
import './ChatInterface.css'

interface Message {
  id: number
  role: string
  content: string
  created_at: string
}

interface Props {
  sessionId: number
  framework: string
  onBack: () => void
}

export default function ChatInterface({ sessionId, framework, onBack }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [reportReady, setReportReady] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load conversation history on mount
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await fetch(`/api/sessions/${sessionId}/messages`)
        const data = await response.json()
        setMessages(data)
        scrollToBottom()
      } catch (err) {
        console.error('Failed to load messages:', err)
      }
    }

    loadMessages()
    // Send initial prompt based on framework
    sendInitialMessage()
  }, [sessionId])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendInitialMessage = async () => {
    try {
      const initialPrompt = `I want to perform threat modeling on my web application using the ${framework.toUpperCase()} framework. Let's start with some details about my application architecture.`
      await sendMessage(initialPrompt)
    } catch (err) {
      console.error('Failed to send initial message:', err)
    }
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

      const data = await response.json()

      // Reload messages to get the latest
      const messagesResponse = await fetch(`/api/sessions/${sessionId}/messages`)
      const newMessages = await messagesResponse.json()
      setMessages(newMessages)
      setInputValue('')
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

  const handleGenerateReport = async () => {
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
          <button className="back-button" onClick={onBack}>← Back</button>
          <div>
            <h2>Threat Modeling Chat</h2>
            <p>Framework: <strong>{framework.toUpperCase()}</strong></p>
          </div>
        </div>
        <div className="chat-actions">
          {reportReady && (
            <button className="download-btn" onClick={handleDownloadPDF}>
              📄 Download PDF Report
            </button>
          )}
          {!reportReady && messages.length > 2 && (
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
          placeholder="Describe your application architecture, data flows, or ask a question..."
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading} className="send-button">
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  )
}
