
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from modules.data_processing import load_dataset, compute_kpis, weekly_trends, stage_counts, source_effectiveness
from modules.bottleneck_detector import detect_bottlenecks
from modules.skill_matcher import score_candidate
from modules.report_generator import generate_pdf_report
from modules.email_alerts import send_bottleneck_alerts

st.set_page_config(page_title="Interview Pipeline Insights", page_icon="🧩", layout="wide")
st.title("Hiring Insights Hub")
st.caption("A smart dashboard for recruiters and hiring teams — track candidate progress, detect delays, analyze sourcing performance, and evaluate skill alignment in one place.")

data_path = Path("data/candidate_data.csv")
jd_path = Path("data/sample_jd.txt")
st.sidebar.subheader("Settings")
days_threshold = st.sidebar.slider("Bottleneck threshold (days without movement)", 7, 60, 14, 1)
recipients_input = st.sidebar.text_input("Alert recipients (comma-separated)", "hiringmanager@example.com,recruiter@example.com")

if not data_path.exists():
    st.error("Dataset not found. Please ensure data/candidate_data.csv exists.")
    st.stop()

df = load_dataset(str(data_path))

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Bottlenecks", "Source Insights", "Skills Analyzer"])

with tab1:
    st.subheader("Recruitment Summary")
    kpis = compute_kpis(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Candidates", kpis["total"])
    c2.metric("Avg. Time to Hire (days)", kpis["avg_time_to_hire_days"] or 0)
    c3.metric("Conversion (Offer+Hired / All)", f"{kpis['conversion_pct'] or 0}%")
    c4.metric("Active Roles", df["Role"].nunique())

    sc = stage_counts(df)
    st.plotly_chart(px.bar(sc, labels={"index":"Stage","value":"Count"}), use_container_width=True)

    wk = weekly_trends(df)
    st.plotly_chart(px.line(wk, x="Applied_Date", y="applications", markers=True), use_container_width=True)

    st.write("### Candidate Journey Flow")
    st.caption("Visualizes how candidates move through each hiring stage — from application to final outcomes like Hired or Rejected.")
    stages = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]
    counts = df["Stage"].value_counts().reindex(stages, fill_value=0).tolist()

    labels = stages
    source = [0, 1, 2, 3, 3]
    target = [1, 2, 3, 4, 5]

    values = [
        counts[1],
        counts[2],
        counts[3],
        counts[4],
        counts[5],
       ]
    node_colors = ["#6AAED6", "#A2C8E6", "#D6B3E6", "#F2B5A8", "#A8E6A3", "#E6D1A3"]
    sankey_fig = go.Figure(
      data=[
        go.Sankey(
            node=dict(
                label=labels,
                pad=25,
                thickness=20,
                color=node_colors,
                line=dict(color="gray", width=0.5),
                hovertemplate='%{label}<extra></extra>',
            ),
            link=dict(source=source, target=target, value=values, color="lightgray"),
        )
        ]
    )

    sankey_fig.update_layout(
    font=dict(size=14, color="#2F2F2F"),
    height=450,
     )

    st.plotly_chart(sankey_fig, use_container_width=True)
    st.write("### Export")
    if st.button("📄 Download PDF Summary", type="primary"):
        pdf_path = "pipeline_summary.pdf"
        generate_pdf_report(pdf_path, kpis, sc, detect_bottlenecks(df, days_threshold))
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="pipeline_summary.pdf", mime="application/pdf")

    st.write("### Candidate Table")
    role_filter = st.multiselect("Filter by Role", sorted(df["Role"].unique()), default=list(df["Role"].unique()))
    stage_filter = st.multiselect("Filter by Stage", sorted(df["Stage"].unique()), default=list(df["Stage"].unique()))
    sdf = df[df["Role"].isin(role_filter) & df["Stage"].isin(stage_filter)]
    st.dataframe(sdf.sort_values(by="Last_Updated", ascending=False), use_container_width=True)

with tab2:
    st.subheader("Bottleneck Insights (Idle Candidates Report)")
    st.caption(
        "Shows candidates who have been idle in early stages for more than the defined threshold. "
        "Use this to take quick action and prevent delays in hiring."
    )
    stuck = detect_bottlenecks(df, days_threshold=days_threshold)
    st.write(f"Candidates in early stages for ≥ {days_threshold} days")
    st.dataframe(stuck[["Candidate","Role","Stage","Source","Applied_Date","Last_Updated","Skills"]], use_container_width=True)

    if st.button("Send Alerts (Simulated)"):
        recips = [r.strip() for r in recipients_input.split(",") if r.strip()]
        result = send_bottleneck_alerts(stuck, recips)
        st.success(result)

with tab3:
    st.subheader("Source Effectiveness")
    eff = source_effectiveness(df)
    st.plotly_chart(px.bar(eff, x="Source", y="SuccessRate(%)", title="Success Rate by Source"), use_container_width=True)
    st.write("Breakdown by source and stage")
    st.dataframe(eff, use_container_width=True)

with tab4:
    st.subheader("Skills Analyzer")
    jd_text = jd_path.read_text() if jd_path.exists() else ""
    jd_text = st.text_area("Job Description (editable)", jd_text, height=220)
    pick = st.multiselect("Candidates", df["Candidate"].tolist(), default=df["Candidate"].head(10).tolist())
    scored = []
    for cand in pick:
        row = df[df["Candidate"] == cand].iloc[0]
        scored.append({"Candidate": cand, "Role": row["Role"], "Stage": row["Stage"], "Score(%)": score_candidate(row["Skills"], jd_text)})
    if scored:
        s_df = pd.DataFrame(scored).sort_values(by="Score(%)", ascending=False)
        st.dataframe(s_df, use_container_width=True)
    st.caption("This MVP uses keyword overlap. For production, swap in spaCy/SentenceTransformers for semantic matching.")
