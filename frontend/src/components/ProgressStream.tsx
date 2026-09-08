import './ProgressStream.css'

interface ProgressEvent {
  type: string
  message?: string
  tool_name?: string
  content?: string
  error?: string
}

interface Props {
  events: ProgressEvent[]
}

export default function ProgressStream({ events }: Props) {
  if (events.length === 0) return null

  return (
    <div className="progress-stream">
      <div className="progress-header">🔄 Analysis Progress</div>
      <div className="progress-events">
        {events.map((event, idx) => (
          <div key={idx} className={`progress-event progress-${event.type}`}>
            <div className="event-icon">
              {event.type === 'start' && '🚀'}
              {event.type === 'text_start' && '✍️'}
              {event.type === 'tool_start' && '🔧'}
              {event.type === 'tool_end' && '✓'}
              {event.type === 'complete' && '✅'}
              {event.type === 'error' && '❌'}
              {event.type === 'text_chunk' && '📝'}
            </div>
            <div className="event-content">
              {event.message && <div className="event-message">{event.message}</div>}
              {event.tool_name && (
                <div className="event-tool">
                  Tool: <code>{event.tool_name}</code>
                </div>
              )}
              {event.error && <div className="event-error">{event.error}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
