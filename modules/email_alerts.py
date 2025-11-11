
def send_bottleneck_alerts(stuck_df, recipients):
    if stuck_df is None or stuck_df.empty:
        return "No alerts sent — no bottlenecks detected."
    if not recipients:
        return "No alerts sent — no recipients configured."
    count = len(stuck_df)
    rec_list = ", ".join(recipients)
    return f"✅ Simulated: Sent {count} bottleneck alert(s) to: {rec_list}"
