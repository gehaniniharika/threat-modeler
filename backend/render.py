"""Render threat reports in multiple formats"""

import json
from typing import Optional
from pdf_generator import generate_threat_report_pdf

def render_json(threat_report: dict) -> str:
    """Render as pretty JSON"""
    return json.dumps(threat_report, indent=2)

def render_html(threat_report: dict) -> str:
    """Render as HTML"""
    app_name = threat_report.get("application_name", "Application")
    framework = threat_report.get("framework", "Unknown")
    verdict = threat_report.get("verdict", "UNCLEAR")
    summary = threat_report.get("summary", "")
    threats = threat_report.get("threats", [])
    recommendations = threat_report.get("recommendations", [])

    verdict_color = {
        "TRUE_POSITIVE": "#d32f2f",
        "FALSE_POSITIVE": "#388e3c",
        "UNCLEAR": "#f57c00"
    }.get(verdict, "#999")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{app_name} - Threat Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #667eea; }}
            .verdict {{ background: {verdict_color}; color: white; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .verdict-text {{ font-size: 24px; font-weight: bold; }}
            .threat {{ background: #f9f9f9; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; }}
            .threat-title {{ font-weight: bold; color: #333; }}
            .threat-severity {{ display: inline-block; padding: 4px 8px; border-radius: 4px; margin: 0 5px; }}
            .severity-critical {{ background: #d32f2f; color: white; }}
            .severity-high {{ background: #f57c00; color: white; }}
            .severity-medium {{ background: #fbc02d; color: white; }}
            .severity-low {{ background: #388e3c; color: white; }}
            .recommendations {{ background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .rec-item {{ margin: 8px 0; padding-left: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{app_name} - Threat Analysis Report</h1>
            <p><strong>Framework:</strong> {framework}</p>
            <p><strong>Summary:</strong> {summary}</p>

            <div class="verdict">
                <div class="verdict-text">Verdict: {verdict.replace('_', ' ')}</div>
                <div>Confidence: {threat_report.get('confidence', 'N/A')}%</div>
            </div>

            <h2>Identified Threats</h2>
            {''.join([f'''
            <div class="threat">
                <div class="threat-title">{t.get('title', 'Unknown')}</div>
                <div><span class="threat-severity severity-{t.get('severity', 'low').lower()}">{t.get('severity', 'Low')}</span></div>
                <p>{t.get('description', '')}</p>
                <p><strong>Affected Component:</strong> {t.get('affected_component', 'N/A')}</p>
                <p><strong>Mitigation:</strong> {t.get('mitigation', 'N/A')}</p>
            </div>
            ''' for t in threats])}

            <div class="recommendations">
                <h2>Recommendations</h2>
                {''.join([f'<div class="rec-item">{i+1}. {rec}</div>' for i, rec in enumerate(recommendations)])}
            </div>
        </div>
    </body>
    </html>
    """

    return html

def render_markdown(threat_report: dict) -> str:
    """Render as Markdown"""
    app_name = threat_report.get("application_name", "Application")
    framework = threat_report.get("framework", "Unknown")
    verdict = threat_report.get("verdict", "UNCLEAR")
    summary = threat_report.get("summary", "")
    threats = threat_report.get("threats", [])
    recommendations = threat_report.get("recommendations", [])
    confidence = threat_report.get("confidence", "N/A")

    md = f"""# {app_name} - Threat Analysis Report

**Framework:** {framework}
**Verdict:** {verdict.replace('_', ' ')}
**Confidence:** {confidence}%

## Summary

{summary}

## Identified Threats

"""

    for i, threat in enumerate(threats, 1):
        md += f"""### Threat {i}: {threat.get('title', 'Unknown')}

- **Severity:** {threat.get('severity', 'Unknown')}
- **Category:** {threat.get('category', threat.get('stage', 'N/A'))}
- **Affected Component:** {threat.get('affected_component', 'N/A')}
- **Description:** {threat.get('description', 'N/A')}
- **Attack Vector:** {threat.get('attack_vector', threat.get('attack_path', 'N/A'))}
- **Mitigation:** {threat.get('mitigation', threat.get('countermeasures', ['N/A'])[0] if isinstance(threat.get('countermeasures'), list) else 'N/A')}

"""

    md += "## Recommendations\n\n"
    for i, rec in enumerate(recommendations, 1):
        md += f"{i}. {rec}\n"

    return md

def render_csv(threat_report: dict) -> str:
    """Render threats as CSV"""
    threats = threat_report.get("threats", [])

    csv = "ID,Title,Category,Severity,Affected Component,Description,Mitigation\n"

    for threat in threats:
        threat_id = threat.get("id", "")
        title = threat.get("title", "").replace('"', '""')
        category = threat.get("category", threat.get("stage", ""))
        severity = threat.get("severity", "")
        component = threat.get("affected_component", "").replace('"', '""')
        description = threat.get("description", "").replace('"', '""')
        mitigation = threat.get("mitigation", "").replace('"', '""')

        csv += f'{threat_id},"{title}","{category}","{severity}","{component}","{description}","{mitigation}"\n'

    return csv
