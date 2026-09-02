"""STRIDE threat modeling framework skill"""

STRIDE_SYSTEM_PROMPT = """Use STRIDE framework to identify threats:
- S: Spoofing (fake identity/auth)
- T: Tampering (modify data/code)
- R: Repudiation (deny actions)
- I: Information Disclosure (expose secrets)
- D: Denial of Service (crash/unavailable)
- E: Elevation of Privilege (unauthorized access)

For each threat: categorize it (S/T/R/I/D/E), describe it, rate severity, suggest fix."""

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
