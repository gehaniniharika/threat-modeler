"""PASTA threat modeling framework skill"""

PASTA_SYSTEM_PROMPT = """Use PASTA framework (7 stages):
1. Assets - What needs protection?
2. Threats - What attacks exist?
3. Vulnerabilities - What weaknesses?
4. Attack paths - How to exploit?
5. Impact - Business consequence?
6. Countermeasures - What fixes?
7. Prioritize - What's most critical?

For each threat: describe attack path, business impact, severity, recommended fix."""

def get_pasta_system_prompt():
    return PASTA_SYSTEM_PROMPT

def format_pasta_threat(threat: dict) -> dict:
    """Format threat for PASTA framework"""
    pasta_stages = {
        'stakeholder': 'Stage 1: Stakeholder & Asset Definition',
        'threat': 'Stage 2: Threat Analysis',
        'vulnerability': 'Stage 3: Vulnerability Analysis',
        'attack': 'Stage 4: Attack Analysis',
        'impact': 'Stage 5: Impact Analysis',
        'countermeasure': 'Stage 6: Countermeasure',
        'ranking': 'Stage 7: Risk Ranking'
    }

    if 'category' in threat:
        stage = threat['category'].lower()
        threat['category'] = pasta_stages.get(stage, threat['category'])

    return threat
