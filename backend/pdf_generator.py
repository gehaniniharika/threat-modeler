from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io

def generate_threat_report_pdf(threat_data: dict) -> bytes:
    """Generate a PDF report from threat modeling data."""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )

    elements = []

    # Title
    title = Paragraph("🛡️ Threat Modeling Report", title_style)
    elements.append(title)

    # Metadata
    app_name = threat_data.get('application_name', 'Unknown Application')
    framework = threat_data.get('framework', 'Unknown')

    metadata = f"""
    <b>Application:</b> {app_name}<br/>
    <b>Framework:</b> {framework.upper()}<br/>
    <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    """
    elements.append(Paragraph(metadata, normal_style))
    elements.append(Spacer(1, 0.3*inch))

    # Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    summary = threat_data.get('summary', 'No summary available')
    elements.append(Paragraph(summary, normal_style))
    elements.append(Spacer(1, 0.2*inch))

    # Threats Section
    threats = threat_data.get('threats', [])
    if threats:
        elements.append(Paragraph(f"Identified Threats ({len(threats)})", heading_style))

        for idx, threat in enumerate(threats, 1):
            threat_text = f"""
            <b>T{idx:03d}: {threat.get('title', 'Unknown')}</b><br/>
            <b>Severity:</b> <font color="{_get_severity_color(threat.get('severity', 'Low'))}">{threat.get('severity', 'Low').upper()}</font><br/>
            <b>Category:</b> {threat.get('category', 'Unknown')}<br/>
            <b>Description:</b> {threat.get('description', 'N/A')}<br/>
            <b>Attack Vector:</b> {threat.get('attack_vector', 'N/A')}<br/>
            <b>Mitigation:</b> {threat.get('mitigation', 'N/A')}<br/>
            """
            elements.append(Paragraph(threat_text, normal_style))
            elements.append(Spacer(1, 0.1*inch))

        elements.append(PageBreak())

    # Data Flows Section
    data_flows = threat_data.get('data_flows', [])
    if data_flows:
        elements.append(Paragraph("Data Flows & Risks", heading_style))

        flow_data = [['Source', 'Destination', 'Data Type', 'Protocol', 'Risks']]
        for flow in data_flows:
            risks = ', '.join(flow.get('risks', [])) or 'None identified'
            flow_data.append([
                flow.get('source', ''),
                flow.get('destination', ''),
                flow.get('data_type', ''),
                flow.get('protocol', ''),
                risks
            ])

        table = Table(flow_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 0.8*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

    # Recommendations Section
    recommendations = threat_data.get('recommendations', [])
    if recommendations:
        elements.append(Paragraph("Key Recommendations", heading_style))

        rec_list = "<br/>".join([f"• {rec}" for rec in recommendations])
        elements.append(Paragraph(rec_list, normal_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def _get_severity_color(severity: str) -> str:
    """Get color code for severity level."""
    colors_map = {
        'critical': '#d32f2f',
        'high': '#f57c00',
        'medium': '#fbc02d',
        'low': '#388e3c'
    }
    return colors_map.get(severity.lower(), '#666666')
