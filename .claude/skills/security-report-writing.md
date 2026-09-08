# Security Report Writing Skill

## Purpose
Create clear, actionable security reports that communicate findings to technical and non-technical audiences.

## When to Use
- Writing threat modeling reports
- Security assessment reporting
- Executive summaries
- Vulnerability disclosures
- Compliance documentation

## Report Structure

### 1. Executive Summary (1-2 pages)
**Audience**: Management, business stakeholders

**Include**:
- Overall security rating
- Critical findings count
- Key recommendations
- Business impact
- Remediation timeline

**Example**:
```
Security Assessment Summary
Application: PaymentGateway v2.1
Assessment Date: 2026-03-15
Overall Rating: HIGH RISK

Key Findings:
- 3 Critical vulnerabilities
- 8 High-risk issues
- 12 Medium-risk findings

Recommended Actions:
1. Address authentication bypass (Critical) - 1 week
2. Fix SQL injection (Critical) - 1 week
3. Implement rate limiting (High) - 2 weeks

Business Impact:
Without remediation, the system is at significant risk of:
- Data breach affecting 10,000+ users
- Financial loss from fraudulent transactions
- Regulatory non-compliance (PCI-DSS, GDPR)
```

### 2. Findings Section
**Audience**: Technical teams, developers

**For Each Finding**:
```
Vulnerability: SQL Injection in User Search
Severity: CRITICAL
CVSS Score: 9.8

Description:
The user search API endpoint accepts unsanitized input
that is directly interpolated into SQL queries. This
allows attackers to execute arbitrary SQL commands.

Location:
File: api/users/search.py, Line 45
Endpoint: POST /api/users/search

Attack Vector:
```
curl -X POST http://api/users/search \
  -d '{"name": "admin\"; DROP TABLE users; --"}'
```

Impact:
- Complete database compromise
- User data exfiltration
- Data loss through deletion
- Service unavailability

Remediation:
Replace string interpolation with parameterized queries:
  cursor.execute("SELECT * FROM users WHERE name = ?", (name,))

Priority: CRITICAL - Fix immediately
Effort: LOW - 1-2 hours
Responsible: Backend team
Due Date: 2026-03-22
```

### 3. Architecture Review
**Audience**: Architects, leads

**Include**:
- Architecture diagram (with security zones)
- Data flow analysis
- Trust boundaries
- Design-level risks
- Architectural recommendations

**Example**:
```
Architecture Assessment

Current Design:
[Client] → [API Gateway] → [Microservices] → [Database]
           (Single point of failure)

Risk: API Gateway is single point of failure

Recommendation:
Add redundancy to API Gateway:
- Deploy on multiple availability zones
- Load balance across instances
- Implement automatic failover

Impact: Improves availability, reduces risk
Effort: Medium
Timeline: 2-3 weeks
```

### 4. Recommendations Summary
**Audience**: All stakeholders

**Organize By**:
- Severity (Critical → High → Medium → Low)
- Component affected
- Implementation effort
- Business priority

**Include**:
- What to fix
- Why it's important
- How to fix it
- Timeline and effort

### 5. Appendices

#### A. Detailed Findings
Complete vulnerability documentation with:
- CWE/CVE references
- Code examples
- Testing evidence
- Proof of concept

#### B. Testing Methodology
- Scope and approach
- Tools used
- Testing period
- Coverage metrics

#### C. Glossary
Define technical terms for non-technical readers

#### D. References
- OWASP resources
- Security standards (PCI-DSS, HIPAA, etc.)
- Best practices
- External references

## Writing Guidelines

### For Technical Audiences
- Use precise terminology
- Include code examples
- Provide detailed remediation
- Reference CWE/CVE
- Show PoC when safe

### For Business Audiences
- Use business impact language
- Quantify risks (user impact, financial)
- Explain timeline
- Highlight compliance issues
- Focus on remediation priorities

### For All Audiences
- Use clear, simple language
- Avoid jargon without explanation
- Provide context
- Use visuals (diagrams, tables)
- Make findings actionable

## Report Sections Template

```
# Security Assessment Report

## 1. Executive Summary
- Overall rating
- Key statistics
- Critical findings
- Recommendations
- Timeline

## 2. Assessment Overview
- Scope
- Methodology
- Timeline
- Tools used
- Assessment period

## 3. Findings Summary
- Count by severity
- Distribution by category
- Trend analysis (if comparing versions)
- Most critical areas

## 4. Detailed Findings
- Finding 1 (Critical)
  - Description, impact, location, remediation
- Finding 2 (Critical)
  - Description, impact, location, remediation
- [etc...]

## 5. Architecture Assessment
- Architecture diagram
- Data flows
- Trust boundaries
- Design-level risks
- Recommendations

## 6. Recommendations
- By severity
- Implementation roadmap
- Effort estimates
- Resource requirements

## 7. Compliance Assessment
- Relevant standards
- Gap analysis
- Compliance risks
- Recommendations

## 8. Appendices
- Detailed technical findings
- Methodology
- Tools and techniques
- References
```

## Severity-Based Messaging

### CRITICAL
```
IMMEDIATE ACTION REQUIRED
This vulnerability represents an imminent threat.
Exploitation is straightforward and impact is severe.
This must be remediated before production deployment.
```

### HIGH
```
URGENT ATTENTION REQUIRED
This vulnerability should be remediated as soon as possible.
Production systems with this vulnerability are at significant risk.
Target remediation within 2 weeks.
```

### MEDIUM
```
SHOULD BE ADDRESSED
This vulnerability should be included in near-term planning.
Consider remediation within 30-60 days.
May impact compliance or future scalability.
```

### LOW
```
CONSIDER FOR IMPROVEMENT
This can be addressed during regular maintenance cycles.
Lower priority but still worth fixing.
May improve defense-in-depth posture.
```

## Metrics to Include

| Metric | Example |
|--------|---------|
| Total Findings | 23 issues found |
| By Severity | 3 Critical, 8 High, 10 Medium, 2 Low |
| By Category | 8 Auth, 6 Injection, 4 Crypto, 5 Other |
| Coverage | 85% of application tested |
| High-Risk Endpoints | 12 of 47 endpoints |
| Remediable Issues | 21 of 23 (91%) |

## Sample Recommendations Format

| # | Finding | Severity | Remediation | Effort | Timeline |
|---|---------|----------|-------------|--------|----------|
| 1 | Auth Bypass | CRITICAL | Implement MFA | Medium | 2 weeks |
| 2 | SQL Injection | CRITICAL | Use parameterized queries | Low | 1 week |
| 3 | Weak Encryption | HIGH | Upgrade to AES-256 | Medium | 2 weeks |

## Tips for Effective Reporting

- [ ] Lead with business impact
- [ ] Provide clear evidence
- [ ] Offer practical solutions
- [ ] Include timeline estimates
- [ ] Highlight compliance issues
- [ ] Use consistent formatting
- [ ] Provide metrics and trends
- [ ] Make findings actionable
- [ ] Maintain professional tone
- [ ] Consider audience knowledge
- [ ] Use visual aids
- [ ] Include implementation roadmap

## Report Review Checklist

- [ ] Findings are accurate
- [ ] Severity ratings are justified
- [ ] Remediation steps are clear
- [ ] Evidence is documented
- [ ] Business impact is explained
- [ ] Timeline is realistic
- [ ] Report is well-organized
- [ ] Language is clear
- [ ] Visual aids enhance understanding
- [ ] References are complete
