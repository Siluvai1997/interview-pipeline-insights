
import pandas as pd

STAGE_ORDER = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]

def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Applied_Date"] = pd.to_datetime(df["Applied_Date"], errors="coerce")
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce")
    return df

def compute_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    by_stage = df["Stage"].value_counts().to_dict()
    tth = None
    hired = df[df["Stage"] == "Hired"]
    if not hired.empty:
        tth = (hired["Last_Updated"] - hired["Applied_Date"]).dt.days.mean().round(1)
    conversion = round(((by_stage.get("Offer",0) + by_stage.get("Hired",0)) / total) * 100, 2) if total else 0
    return {"total": total, "by_stage": by_stage, "avg_time_to_hire_days": tth, "conversion_pct": conversion}

def weekly_trends(df: pd.DataFrame):
    return df.set_index("Applied_Date").resample("W-MON").size().reset_index(name="applications")

def stage_counts(df: pd.DataFrame):
    return df["Stage"].value_counts().reindex(STAGE_ORDER, fill_value=0)

def source_effectiveness(df: pd.DataFrame):
    by_source = df.pivot_table(index="Source", columns="Stage", aggfunc="size", fill_value=0)
    by_source["Success"] = by_source.get("Offer", 0) + by_source.get("Hired", 0)
    by_source["Total"] = by_source.sum(axis=1)
    by_source["SuccessRate(%)"] = (by_source["Success"] / by_source["Total"]).replace([float("inf")], 0) * 100
    return by_source.reset_index()
