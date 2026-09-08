# Architecture Analysis Skill

## Purpose
Analyze application architecture for security implications and design flaws.

## When to Use
- Architecture review
- Design validation
- Microservices security assessment
- Deployment model evaluation
- Integration point analysis

## Architecture Assessment Checklist

### 1. System Boundaries & Trust
- [ ] Identify trust boundaries
- [ ] Map external systems
- [ ] Define security perimeters
- [ ] Assess network segmentation
- [ ] Evaluate isolation mechanisms

### 2. Authentication & Authorization
- [ ] Authentication method (OAuth, SAML, custom)
- [ ] Token/session management
- [ ] Multi-factor authentication
- [ ] Role-based access control
- [ ] Cross-service authorization

### 3. Data Protection
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management strategy
- [ ] Data classification
- [ ] Retention and disposal

### 4. API Security
- [ ] API authentication
- [ ] Rate limiting
- [ ] Input validation
- [ ] Output encoding
- [ ] API versioning strategy

### 5. Dependency Management
- [ ] Third-party libraries
- [ ] Open source risks
- [ ] Update strategy
- [ ] Vulnerability scanning
- [ ] Supply chain risks

### 6. Logging & Monitoring
- [ ] Event logging coverage
- [ ] Log retention
- [ ] Log protection
- [ ] Alerting mechanisms
- [ ] Compliance logging

### 7. Deployment & Infrastructure
- [ ] Environment isolation
- [ ] Container security
- [ ] Cloud configuration
- [ ] Secrets management
- [ ] Infrastructure as code

### 8. Resilience & Availability
- [ ] Failover mechanisms
- [ ] Load balancing
- [ ] Backup/recovery
- [ ] DDoS protection
- [ ] Rate limiting

## Common Architecture Patterns & Risks

### Monolithic Application
**Risks**:
- Single point of failure
- Broad attack surface
- Difficult to isolate compromises
- Scaling challenges

**Recommendations**:
- Segment by security boundary
- Implement defense-in-depth
- Strong authentication/authorization
- Comprehensive logging

### Microservices
**Risks**:
- Inter-service communication complexity
- Distributed secrets management
- Network-based attacks
- Service-to-service auth

**Recommendations**:
- Service mesh security
- Mutual TLS between services
- API gateway authentication
- Distributed tracing

### Serverless/FaaS
**Risks**:
- Shared infrastructure
- Ephemeral nature
- Privilege management
- Cold start vulnerabilities

**Recommendations**:
- Minimize function scope
- Least privilege IAM
- Secure environment variables
- Request validation

### Client-Side Heavy (SPA)
**Risks**:
- Client secrets exposure
- Authentication bypass
- XSS vulnerabilities
- Storage vulnerabilities

**Recommendations**:
- Server-side validation
- CSP headers
- Secure token storage
- HTTPS enforcement

## Security Architecture Patterns

### Defense in Depth
Multiple layers of security:
1. Perimeter (firewall, WAF)
2. Network (segmentation, VPN)
3. Application (authentication, authorization)
4. Data (encryption, masking)

### Zero Trust Architecture
- Verify every request
- Assume no implicit trust
- Principle of least privilege
- Continuous validation

### Secure by Design
- Security requirements early
- Threat modeling in design phase
- Security reviews before coding
- Testing throughout development

## Data Flow Analysis

### Key Questions
- Where does sensitive data flow?
- What transformations occur?
- Where is data at rest?
- Who has access?
- Are flows encrypted?

### Sensitive Data Identification
- Personal data (names, emails, phones)
- Financial data (payments, accounts)
- Authentication data (passwords, tokens)
- Health/medical data
- Business secrets

## Component Interaction Matrix

| From | To | Data | Auth | Encryption |
|------|-----|------|------|------------|
| Web | API | JSON | JWT | HTTPS |
| API | DB | SQL | mTLS | TLS |
| API | Cache | JSON | - | TLS |
| Worker | Queue | JSON | - | - |

## Output Format

```json
{
  "application_name": "string",
  "architecture_type": "monolithic|microservices|serverless|hybrid",
  "summary": "Overall security posture",
  "components": [
    {
      "name": "Component name",
      "type": "API|Database|Cache|Queue|etc",
      "criticality": "Critical|High|Medium|Low",
      "authentication": "Method",
      "encryption": "At rest|In transit|Both|None",
      "risks": ["Risk 1", "Risk 2"]
    }
  ],
  "data_flows": [
    {
      "source": "Component A",
      "destination": "Component B",
      "data_type": "Sensitive|Internal|Public",
      "encrypted": true,
      "risks": []
    }
  ],
  "architecture_risks": ["Risk 1", "Risk 2"],
  "recommendations": ["Rec 1", "Rec 2"]
}
```

## Analysis Checklist
- [ ] All components identified
- [ ] Trust boundaries mapped
- [ ] Data flows documented
- [ ] Authentication mechanisms reviewed
- [ ] Encryption strategy validated
- [ ] Dependencies assessed
- [ ] Logging coverage verified
- [ ] Resilience evaluated
- [ ] Risks documented
- [ ] Recommendations provided

## Tips
- Draw the architecture first
- Identify data flows explicitly
- Mark trust boundaries clearly
- Consider attacker movement
- Evaluate defense layers
- Think about failure scenarios
- Consider compliance requirements
- Validate assumptions with team
