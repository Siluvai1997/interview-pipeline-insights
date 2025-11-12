import matplotlib.pyplot as plt
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_report(df, kpis):
    """Generate an enhanced PDF summary report for Hiring Insights Hub."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Title and timestamp
    elements.append(Paragraph("<b>Hiring Insights Hub — Summary Report</b>", styles["Title"]))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # KPIs
    elements.append(Paragraph("<b>Key Metrics</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Total Candidates: {kpis['total']}", styles["Normal"]))
    elements.append(Paragraph(f"Avg. Time to Hire (days): {round(kpis['avg_time_to_hire_days'], 1)}", styles["Normal"]))
    elements.append(Paragraph(f"Conversion (Offer+Hired / All): {round(kpis['conversion_pct'], 2)}%", styles["Normal"]))
    elements.append(Spacer(1, 16))

    # Candidates by Stage Chart (with numeric labels)
    fig, ax = plt.subplots(figsize=(4, 3))
    stage_counts = df["Stage"].value_counts().sort_index()
    ax.bar(stage_counts.index, stage_counts.values, color="#1f77b4")
    ax.set_title("Candidates by Stage")
    ax.set_xlabel("Stage")
    ax.set_ylabel("Count")

    for i, v in enumerate(stage_counts.values):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    img_stage = BytesIO()
    plt.savefig(img_stage, format='png', bbox_inches='tight')
    plt.close(fig)
    img_stage.seek(0)
    elements.append(Paragraph("<b>Candidates by Stage</b>", styles["Heading2"]))
    elements.append(Image(img_stage, width=250, height=200))
    elements.append(Spacer(1, 12))

    # Candidates by Source Chart
    fig, ax = plt.subplots(figsize=(4, 3))
    source_counts = df["Source"].value_counts().sort_index()
    ax.bar(source_counts.index, source_counts.values, color="#2ca02c")
    ax.set_title("Candidates by Source")
    ax.set_xlabel("Source")
    ax.set_ylabel("Count")

    for i, v in enumerate(source_counts.values):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    img_source = BytesIO()
    plt.savefig(img_source, format='png', bbox_inches='tight')
    plt.close(fig)
    img_source.seek(0)
    elements.append(Paragraph("<b>Candidates by Source</b>", styles["Heading2"]))
    elements.append(Image(img_source, width=250, height=200))
    elements.append(Spacer(1, 12))

    # Stage vs Source summary table
    pivot_table = df.pivot_table(index="Source", columns="Stage", aggfunc="size", fill_value=0)
    data = [ ["Source"] + list(pivot_table.columns) ] + [ [src] + list(pivot_table.loc[src]) for src in pivot_table.index ]
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))
    elements.append(Paragraph("<b>Stage Breakdown by Source</b>", styles["Heading2"]))
    elements.append(table)
    elements.append(Spacer(1, 16))

    # Bottleneck candidates summary
    elements.append(Paragraph("<b>Bottlenecks (stuck candidates)</b>", styles["Heading2"]))
    stuck_candidates = df.sort_values(by="Last_Updated").head(10)
    for _, row in stuck_candidates.iterrows():
        line = f"- {row['Candidate']} ({row['Role']}), Stage: {row['Stage']}, Source: {row['Source']}, Last Updated: {row['Last_Updated']}, Applied: {row['Applied_Date']}"
        elements.append(Paragraph(line, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Build and return file
    doc.build(elements)
    buffer.seek(0)
    return buffer
