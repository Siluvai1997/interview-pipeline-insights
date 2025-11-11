
# Interview Pipeline Insights

A modern, data-driven dashboard that helps recruiters and hiring managers track pipeline health, detect bottlenecks, and optimize hiring efficiency — with the precision of a DevOps observability system.

## Live Demo
  [Launch the App on Streamlit Cloud](https://your-final-url-here)

*(The app is free to access — hosted via Streamlit Cloud using this repository.)*

## MVP Features
- Pipeline overview (counts by stage, weekly applications)
- Bottleneck detector (threshold-based)
- Source effectiveness (success rate by channel)
- Skills analyzer (simple keyword overlap; ready to swap for spaCy/SBERT)

## Tech Stack
- **Frontend / UI:** Streamlit (for simplicity and hosting)
- **Data Handling:** Pandas
- **Visualization:** Plotly, Matplotlib, or Altair
- **NLP / Skill Matching:** spaCy or SentenceTransformers (optional)
- **Automation / Alerts:** Python smtplib
- **Storage:** CSV
- **Hosting:** Streamlit Cloud

## Repo Structure
```
interview-pipeline-insights/
├── app.py
├── data/
│   ├── candidate_data.csv
│   └── sample_jd.txt
├── modules/
│   ├── data_processing.py
│   ├── bottleneck_detector.py
│   └── skill_matcher.py
├── requirements.txt
└── README.md
```

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Upload Your Data (CSV Format)
```
Candidate,Role,Stage,Source,Applied_Date,Last_Updated,Skills
John Doe,DevOps Engineer,Interview,LinkedIn,2025-09-12,2025-10-01,Python;AWS;Terraform
Jane Smith,Cloud Engineer,Offer,Referral,2025-09-15,2025-10-10,Azure;Kubernetes;CI/CD
```

## Roadmap
- SLA-based alerts (email/Slack) for stuck candidates
- Sankey funnel visualization with stage conversion
- Semantic skill matching using spaCy / SentenceTransformers
- PDF report export for weekly hiring syncs
