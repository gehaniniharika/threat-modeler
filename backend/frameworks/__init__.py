"""Framework skills for threat modeling"""

from .stride_skill import get_stride_system_prompt, format_stride_threat
from .pasta_skill import get_pasta_system_prompt, format_pasta_threat
from .phantom_b_skill import get_phantom_b_system_prompt, format_phantom_b_threat

FRAMEWORKS = {
    'stride': {
        'name': 'STRIDE',
        'prompt_getter': get_stride_system_prompt,
        'formatter': format_stride_threat,
        'description': 'Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege'
    },
    'pasta': {
        'name': 'PASTA',
        'prompt_getter': get_pasta_system_prompt,
        'formatter': format_pasta_threat,
        'description': 'Process for Attack Simulation and Threat Analysis'
    },
    'phantom-b': {
        'name': 'PHANTOM-B',
        'prompt_getter': get_phantom_b_system_prompt,
        'formatter': format_phantom_b_threat,
        'description': 'Probabilistic Heuristic Attack and Mitigation Model using Behavioral analysis'
    }
}

def get_framework_prompt(framework: str) -> str:
    """Get system prompt for a framework"""
    if framework in FRAMEWORKS:
        return FRAMEWORKS[framework]['prompt_getter']()
    return get_stride_system_prompt()

def format_threat_for_framework(framework: str, threat: dict) -> dict:
    """Format threat for specific framework"""
    if framework in FRAMEWORKS:
        return FRAMEWORKS[framework]['formatter'](threat)
    return threat
