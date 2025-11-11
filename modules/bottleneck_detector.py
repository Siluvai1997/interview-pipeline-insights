
import pandas as pd

def detect_bottlenecks(df: pd.DataFrame, days_threshold: int = 14) -> pd.DataFrame:
    stuck = df[(df["Stage"].isin(["Applied","Screening","Interview"])) &
               ((df["Last_Updated"] - df["Applied_Date"]).dt.days >= days_threshold)]
    return stuck.sort_values(by="Last_Updated", ascending=False).reset_index(drop=True)
