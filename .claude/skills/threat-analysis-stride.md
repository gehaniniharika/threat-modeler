# STRIDE Threat Modeling Skill

## Purpose
Apply the STRIDE framework to systematically identify threats across six categories.

## When to Use
- Structured threat identification
- Security architecture reviews
- Compliance and audit preparation
- Risk assessments requiring categorization

## STRIDE Categories

### S - Spoofing
**Definition**: Illegally accessing and using another user's authentication information

**Questions to ask**:
- How are users authenticated?
- Can identities be forged or impersonated?
- Are credentials stored securely?
- What happens if someone bypasses authentication?

**Threat Examples**:
- Password brute force attacks
- Session hijacking
- API token theft
- Fake admin accounts

### T - Tampering
**Definition**: Malicious modification of data or code

**Questions to ask**:
- Can data be modified in transit?
- Are updates signed/verified?
- Can configuration be changed?
- Is code injection possible?

**Threat Examples**:
- Man-in-the-middle attacks
- Database record modification
- Code injection (SQL, command, template)
- Configuration tampering

### R - Repudiation
**Definition**: Denying responsibility for actions performed

**Questions to ask**:
- Are actions logged?
- Can logs be deleted or modified?
- Are audit trails tamper-proof?
- Can users deny performing actions?

**Threat Examples**:
- Log deletion/tampering
- Unattributed actions
- Missing audit trails
- Disputed transactions

### I - Information Disclosure
**Definition**: Exposure of confidential information

**Questions to ask**:
- What sensitive data exists?
- Is data encrypted at rest and in transit?
- Who can access what data?
- Are error messages revealing?

**Threat Examples**:
- Unauthorized data access
- Sensitive data in logs
- Information leakage in errors
- Cache poisoning

### D - Denial of Service
**Definition**: Making the system unavailable

**Questions to ask**:
- What could crash the system?
- Are there rate limits?
- What's the resource capacity?
- How resilient is the system?

**Threat Examples**:
- Server overload attacks
- Database resource exhaustion
- Network bandwidth saturation
- Algorithm complexity attacks

### E - Elevation of Privilege
**Definition**: Gaining unauthorized access to perform privileged actions

**Questions to ask**:
- How are permissions enforced?
- Can normal users become admins?
- Are privilege checks on every operation?
- What's the impact of privilege escalation?

**Threat Examples**:
- Privilege escalation exploits
- Authorization bypass
- Role confusion attacks
- Insecure direct object reference

## Methodology

### For Each Component:
1. Map to data flows
2. Identify boundaries
3. Apply each STRIDE category
4. Ask category-specific questions
5. Rate severity and likelihood

### Severity Scoring:
- **Critical**: Widespread impact, easy to exploit
- **High**: Significant impact, moderate difficulty
- **Medium**: Moderate impact, requires skill
- **Low**: Minor impact, difficult to exploit

## Output Format
```json
{
  "framework": "STRIDE",
  "threats": [
    {
      "id": "S001",
      "category": "Spoofing",
      "title": "Authentication bypass",
      "severity": "Critical",
      "description": "...",
      "affected_component": "Auth service",
      "attack_vector": "...",
      "mitigation": "..."
    }
  ]
}
```

## Analysis Checklist
- [ ] Reviewed all entry points
- [ ] Checked authentication at each boundary
- [ ] Verified data encryption (transit & rest)
- [ ] Assessed logging and audit trails
- [ ] Evaluated availability and resilience
- [ ] Checked authorization on all operations
- [ ] Prioritized threats by severity
- [ ] Recommended mitigations for each

## Tips
- Go through STRIDE categories systematically
- Don't skip categories even if nothing comes up
- Think from attacker perspective
- Consider both technical and social engineering
- Map threats to specific components
- Link threats to business impact
