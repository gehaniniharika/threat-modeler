interface Framework {
  id: string
  name: string
  description: string
}

interface Props {
  frameworks: Framework[]
  onSelect: (id: string) => void
}

export default function FrameworkSelector({ frameworks, onSelect }: Props) {
  return (
    <section className="framework-selector">
      <div className="selector-content">
        <h2>Choose Threat Modeling Framework</h2>
        <p>Select the framework you'd like to use for threat modeling your application.</p>

        <div className="framework-grid">
          {frameworks.map((fw) => (
            <button
              key={fw.id}
              className="framework-option"
              onClick={() => onSelect(fw.id)}
            >
              <h3>{fw.name}</h3>
              <p>{fw.description}</p>
              <span className="cta">Start Analysis →</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  )
}
