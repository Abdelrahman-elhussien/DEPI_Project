import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data

st.set_page_config(page_title="Subjects", page_icon="📚", layout="wide")
st.title("📚 Subjects")

students, subjects, df = load_data()

if df.empty or "subject" not in df.columns:
    st.warning("No subject data found in scores.")
else:
    st.subheader("Average score by subject")
    agg = df.groupby("subject", dropna=True)["score"].mean().reset_index().sort_values("score", ascending=False)
    chart = (alt.Chart(agg)
               .mark_bar()
               .encode(x=alt.X("subject:N", sort="-y"), y=alt.Y("score:Q", title="Avg score"), tooltip=["subject:N","score:Q"])
               .interactive())
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Enrollment by subject (approximate)")
    # Approximate enrollment = distinct students per subject in scores
    enr = df.groupby("subject")["student_id"].nunique().reset_index(name="students")
    st.bar_chart(enr.set_index("subject"))
    st.dataframe(enr.sort_values("students", ascending=False))
