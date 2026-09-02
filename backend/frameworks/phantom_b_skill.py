"""PHANTOM-B threat modeling framework skill"""

PHANTOM_B_SYSTEM_PROMPT = """Use PHANTOM-B framework (behavioral threat analysis):
- Normal: Define normal user/system behavior
- Anomaly: What deviations indicate threats?
- Probability: Estimate threat likelihood
- Detection: How to monitor/alert?
- Prevention: What controls help?

For each threat: describe behavior pattern, anomaly detection, likelihood, monitoring approach."""

def get_phantom_b_system_prompt():
    return PHANTOM_B_SYSTEM_PROMPT

def format_phantom_b_threat(threat: dict) -> dict:
    """Format threat for PHANTOM-B framework"""
    phantom_categories = {
        'behavioral': 'Behavioral Threat',
        'anomaly': 'Anomaly Detection',
        'probability': 'Probabilistic Assessment',
        'monitoring': 'Behavioral Monitoring',
        'pattern': 'Pattern-based Threat'
    }

    if 'category' in threat:
        category = threat['category'].lower()
        threat['category'] = phantom_categories.get(category, threat['category'])

    return threat
