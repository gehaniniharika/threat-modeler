"""STRIDE threat modeling framework skill"""

STRIDE_SYSTEM_PROMPT = """You are a STRIDE threat modeling expert. STRIDE stands for:
- Spoofing: Illegally accessing and using another user's authentication information
- Tampering: Malicious modification of data or code
- Repudiation: Denying responsibility for an action
- Information Disclosure: Exposure of confidential information
- Denial of Service: Making the system unavailable
- Elevation of Privilege: Gaining unauthorized access to perform privileged actions

Analyze the application architecture using STRIDE categories. For each threat:
1. Map it to a specific STRIDE category
2. Explain the threat in STRIDE terms
3. Rate severity (Critical/High/Medium/Low)
4. Suggest STRIDE-specific mitigations

When generating the report, include all 6 STRIDE categories and identify threats under each.
Format threats with STRIDE category codes (S, T, R, I, D, E) for easy reference."""

def get_stride_system_prompt():
    return STRIDE_SYSTEM_PROMPT

def format_stride_threat(threat: dict) -> dict:
    """Format threat for STRIDE framework"""
    stride_categories = {
        'S': 'Spoofing',
        'T': 'Tampering',
        'R': 'Repudiation',
        'I': 'Information Disclosure',
        'D': 'Denial of Service',
        'E': 'Elevation of Privilege'
    }

    if 'category' in threat:
        threat['category'] = stride_categories.get(threat['category'].upper()[0], threat['category'])

    return threat
