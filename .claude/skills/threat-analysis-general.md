# General Threat Analysis Skill

## Purpose
Perform comprehensive threat analysis on web applications by gathering architecture details and identifying security risks.

## When to Use
- Initial threat modeling engagement
- High-level security review
- Architecture assessment
- Vulnerability discovery

## Methodology

### Phase 1: Information Gathering
Ask about:
- Application purpose and business context
- Architecture and components
- Data flows and integrations
- Authentication/authorization mechanisms
- Technologies and frameworks
- Deployment environment
- User roles and permissions

### Phase 2: Threat Identification
Identify potential threats by analyzing:
- Attack surface (entry points)
- Data sensitivity (PII, secrets, business data)
- Component interactions
- External dependencies
- Trust boundaries

### Phase 3: Risk Assessment
For each threat:
- Severity: Critical / High / Medium / Low
- Likelihood of exploitation
- Potential business impact
- Affected users/data
- Current mitigations (if any)

### Phase 4: Recommendations
Provide:
- Prioritized mitigation strategies
- Implementation guidance
- Detection and monitoring approaches
- Follow-up security measures

## Output Format
```json
{
  "application_name": "string",
  "summary": "Executive summary",
  "threats": [
    {
      "id": "G001",
      "title": "Threat title",
      "description": "Detailed description",
      "severity": "Critical|High|Medium|Low",
      "affected_component": "Component name",
      "attack_vector": "How it could be exploited",
      "potential_impact": "Consequences",
      "mitigation": "Recommended fix"
    }
  ],
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}
```

## Example Prompt
```
Analyze this web application for security threats:
- Backend: Node.js/Express API
- Frontend: React SPA
- Database: PostgreSQL
- Auth: JWT in localStorage
- Users: Admin, Editor, Viewer roles

Key data: User profiles, payment info, medical records
```

## Tips
- Ask clarifying questions to understand the full picture
- Prioritize threats by business impact
- Consider both technical and organizational factors
- Suggest practical mitigations, not just theory
- Think about attacker perspectives and motivations
