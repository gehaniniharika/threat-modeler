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
  const [uploadingFile, setUploadingFile] = useState(false)
  const [showExportMenu, setShowExportMenu] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const exportFormats = [
    { label: "📄 PDF", format: "pdf", mime: "application/pdf" },
    { label: "📋 JSON", format: "json", mime: "application/json" },
    { label: "🌐 HTML", format: "html", mime: "text/html" },
    { label: "📝 Markdown", format: "markdown", mime: "text/markdown" },
    { label: "📊 CSV", format: "csv", mime: "text/csv" }
  ]

  const GREETING_MESSAGE = {
    id: 0,
    role: 'assistant',
    content: "Hi! I'm ThreatModeler, your AI threat modeling assistant. Please describe your web application - tell me about its architecture, main components, data flows, authentication methods, and technologies you're using. I'll help you identify potential threats and vulnerabilities.",
    created_at: new Date().toISOString()
  }

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

  const handleExport = async (format: string) => {
    try {
      const endpoint = format === 'pdf' ? 'download-pdf' : `download-${format}`
      const response = await fetch(`/api/sessions/${sessionId}/${endpoint}`)

      if (!response.ok) throw new Error('Export failed')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url

      const ext = format === 'markdown' ? 'md' : format
      a.download = `threat_report_${sessionId}.${ext}`
      a.click()
      window.URL.revokeObjectURL(url)
      setShowExportMenu(false)
    } catch (err) {
      console.error(`Failed to export as ${format}:`, err)
      alert(`Error exporting as ${format}`)
    }
  }

  const handleCopyToClipboard = async () => {
    try {
      const response = await fetch(`/api/sessions/${sessionId}/report?format=json`)
      const data = await response.json()
      await navigator.clipboard.writeText(data.content)
      alert('Report copied to clipboard!')
      setShowExportMenu(false)
    } catch (err) {
      console.error('Failed to copy:', err)
      alert('Error copying to clipboard')
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploadingFile(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`/api/sessions/${sessionId}/upload-file`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to upload file')
      }

      // Reload messages to get the latest
      const messagesResponse = await fetch(`/api/sessions/${sessionId}/messages`)
      const newMessages = await messagesResponse.json()
      setMessages(newMessages)

      // Show framework selector if needed
      if (newMessages.length >= 4 && !selectedFramework && !showFrameworkSelector) {
        setShowFrameworkSelector(true)
      }
    } catch (err) {
      console.error('Failed to upload file:', err)
      alert(`Error: ${err instanceof Error ? err.message : 'Failed to upload file'}`)
    } finally {
      setUploadingFile(false)
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
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
            <div className="export-menu-container">
              <button
                className="export-btn"
                onClick={() => setShowExportMenu(!showExportMenu)}
              >
                📥 Export Report ▼
              </button>
              {showExportMenu && (
                <div className="export-dropdown">
                  {exportFormats.map(fmt => (
                    <button
                      key={fmt.format}
                      className="export-option"
                      onClick={() => handleExport(fmt.format)}
                    >
                      {fmt.label}
                    </button>
                  ))}
                  <div className="export-divider"></div>
                  <button
                    className="export-option"
                    onClick={handleCopyToClipboard}
                  >
                    📋 Copy JSON
                  </button>
                </div>
              )}
            </div>
          )}
          {selectedFramework && !reportReady && messages.length > 4 && (
            <button className="generate-btn" onClick={handleGenerateReport} disabled={loading}>
              {loading ? 'Generating...' : '✓ Generate Report'}
            </button>
          )}
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div className={`message ${GREETING_MESSAGE.role}`}>
            <div className="message-content">
              🤖 {GREETING_MESSAGE.content}
            </div>
          </div>
        )}

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
          disabled={loading || showFrameworkSelector || uploadingFile}
          className="chat-input"
        />

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          accept=".pdf,.docx,.doc"
          disabled={loading || uploadingFile}
          className="file-input"
          style={{ display: 'none' }}
        />

        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={loading || uploadingFile || showFrameworkSelector}
          className="file-button"
          title="Upload PDF or Word document"
        >
          {uploadingFile ? '⏳' : '📎'}
        </button>

        <button type="submit" disabled={loading || showFrameworkSelector || uploadingFile} className="send-button">
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  )
}
