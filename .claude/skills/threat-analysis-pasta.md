# PASTA Threat Modeling Skill

## Purpose
Apply the PASTA (Process for Attack Simulation and Threat Analysis) framework to identify threats through attack simulation.

## When to Use
- Attack-focused threat modeling
- Detailed threat scenario analysis
- Business impact assessment
- Risk prioritization by likelihood

## PASTA Methodology - 7 Stages

### Stage 1: Stakeholder and Asset Definition
**Goal**: Identify what needs protection and why

**Key Questions**:
- What assets does the application manage?
- Who are the stakeholders?
- What's the business value of the application?
- What compliance requirements exist?
- What's the impact of a security breach?

**Outcomes**:
- Asset inventory
- Business objectives
- Compliance requirements
- Impact severity baseline

### Stage 2: Threat Analysis
**Goal**: Identify existing and potential threats

**Key Questions**:
- What external threats exist?
- What insider threats are possible?
- What's the threat landscape?
- Who might want to attack this?
- What's their motivation?

**Outcomes**:
- Threat actors identified
- Attack motivations documented
- Historical threat patterns
- Emerging threat landscape

### Stage 3: Vulnerability Analysis
**Goal**: Find weaknesses that can be exploited

**Key Questions**:
- What vulnerabilities exist in the code?
- Are dependencies vulnerable?
- What configuration weaknesses exist?
- Are there architectural flaws?
- What's the attack surface?

**Outcomes**:
- Vulnerability inventory
- Severity ratings
- Exploitability assessment
- Root cause analysis

### Stage 4: Attack Analysis
**Goal**: Simulate how attacks would work

**Key Questions**:
- How would an attacker exploit each vulnerability?
- What's the step-by-step attack path?
- What tools/skills are needed?
- How detectable is the attack?
- What resources are required?

**Outcomes**:
- Attack scenarios
- Attack trees
- Likelihood assessment
- Complexity evaluation

### Stage 5: Impact Analysis
**Goal**: Assess business consequences

**Key Questions**:
- If exploited, what happens?
- Who is affected (users, business)?
- What's the financial impact?
- What's the reputational damage?
- What's the compliance impact?

**Outcomes**:
- Impact scenarios
- Business loss quantification
- Affected stakeholders
- Regulatory consequences

### Stage 6: Countermeasure Recommendations
**Goal**: Recommend mitigations and controls

**Key Questions**:
- What controls would prevent this?
- Can it be detected?
- Can it be recovered from?
- What's the implementation cost?
- What's the operational overhead?

**Outcomes**:
- Prevention controls
- Detection mechanisms
- Response procedures
- Residual risk assessment

### Stage 7: Risk Ranking and Reporting
**Goal**: Prioritize and communicate findings

**Key Questions**:
- Which threats are highest priority?
- What's the ranking methodology?
- How should this be communicated?
- What's the remediation roadmap?

**Outcomes**:
- Risk rankings
- Executive summary
- Detailed threat descriptions
- Remediation roadmap

## Methodology Flow

```
Asset Definition → Threat Analysis → Vulnerability → Attack Simulation
         ↓                ↓                  ↓              ↓
   What protects?   Who attacks?      What's broken?   How attack works?
         ↓                ↓                  ↓              ↓
         └──────────────────────────────────────────────────┘
                         ↓
                  Impact Analysis
                  Business consequence?
                         ↓
              Countermeasure Recommendations
              Prevention + Detection + Response
                         ↓
              Risk Ranking and Reporting
              Prioritize and communicate
```

## Output Format
```json
{
  "framework": "PASTA",
  "application_name": "App name",
  "stage_1": {"assets": [], "objectives": []},
  "stage_2": {"threats": [], "threat_actors": []},
  "stage_3": {"vulnerabilities": []},
  "stage_4": {"attack_paths": []},
  "stage_5": {"business_impact": []},
  "stage_6": {"countermeasures": []},
  "stage_7": {"risk_rankings": []}
}
```

## Attack Tree Example
```
Goal: Steal user data
├── Compromise authentication
│   ├── Brute force passwords
│   ├── Exploit session handling
│   └── Steal credentials
├── Exploit authorization
│   ├── Privilege escalation
│   └── Insecure direct object reference
└── Exploit data handling
    ├── SQL injection
    └── Unencrypted data transmission
```

## Risk Scoring

**Likelihood**: Very High → High → Medium → Low → Very Low
**Impact**: Critical → High → Medium → Low → Minimal
**Risk = Likelihood × Impact**

## Analysis Checklist
- [ ] Stakeholders and assets identified
- [ ] Threat landscape documented
- [ ] Vulnerabilities cataloged
- [ ] Attack scenarios simulated
- [ ] Business impact assessed
- [ ] Countermeasures recommended
- [ ] Risks ranked
- [ ] Report prepared

## Tips
- Ground threats in real attack scenarios
- Quantify business impact
- Think like an attacker
- Consider the attack chain
- Map vulnerabilities to specific assets
- Prioritize by exploitability and impact
- Provide specific remediation steps
