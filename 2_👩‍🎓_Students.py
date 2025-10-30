import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data

st.set_page_config(page_title="Students", page_icon="👩‍🎓", layout="wide")
st.title("👩‍🎓 Students")

students, subjects, df = load_data()

if students.empty:
    st.warning("No students found.")
else:
    # Basic searchable table
    q = st.text_input("Search name or ID")
    sview = students.copy()
    if q:
        ql = q.lower()
        sview = sview[sview.astype(str).apply(lambda r: ql in r.str.lower().to_string(), axis=1)]
    st.dataframe(sview, use_container_width=True)

    # If scores available, show per-student stats
    if not df.empty and "student_id" in df.columns:
        st.subheader("Per-student average")
        ag = df.groupby(["student_id"]).agg(avg_score=("score","mean"), records=("score","count")).reset_index()
        ag = ag.merge(students[["student_id","name"]], on="student_id", how="left")
        chart = (alt.Chart(ag)
                   .mark_circle()
                   .encode(x="records:Q", y=alt.Y("avg_score:Q", title="Avg score"),
                           size=alt.Size("records:Q", legend=None), tooltip=["name:N","avg_score:Q","records:Q"])
                   .interactive())
        st.altair_chart(chart, use_container_width=True)
