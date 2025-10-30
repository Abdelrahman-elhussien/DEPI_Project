import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils import load_data

st.set_page_config(page_title="Attendance", page_icon="🗓️", layout="wide")
st.title("🗓️ Attendance")

students, subjects, df = load_data()

# If attendance not in CSVs, derive a proxy using presence of score records per day
if df.empty or "date" not in df.columns:
    st.info("Attendance features need either an `attendance` column or dated `scores`. Showing a placeholder heatmap.")
    # Placeholder calendar-like heatmap with random values (so UI works).
    dates = pd.date_range(pd.to_datetime("today") - pd.Timedelta(days=27), periods=28, freq="D")
    att = pd.DataFrame({"date": dates, "attendance_rate": np.random.uniform(0.6, 0.98, len(dates))})
else:
    # Compute daily attendance rate = distinct students with records that day / total students
    daily = df.groupby("date")["student_id"].nunique().reset_index(name="present_students")
    total = len(students) if len(students) > 0 else daily["present_students"].max()
    att = daily.assign(attendance_rate=daily["present_students"] / max(total,1))

st.subheader("Daily attendance rate")
chart = (alt.Chart(att).mark_area(opacity=0.3).encode(
    x="date:T", y=alt.Y("attendance_rate:Q", axis=alt.Axis(format="%")),
    tooltip=[alt.Tooltip("date:T"), alt.Tooltip("attendance_rate:Q", format=".1%")]
).interactive())
st.altair_chart(chart, use_container_width=True)

st.dataframe(att.tail(30))
