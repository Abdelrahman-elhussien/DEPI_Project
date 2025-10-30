import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Advanced Analytics")

students, subjects, df = load_data()

if df.empty:
    st.warning("No data available.")
else:
    st.subheader("Score categories")
    cats = pd.cut(df["score"], bins=[-1,59,79,100], labels=["Low","Medium","High"]).value_counts().reset_index()
    cats.columns = ["category","count"]
    st.bar_chart(cats.set_index("category"))

    st.subheader("Monthly averages by subject")
    if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
        d2 = df.copy()
        d2["month"] = d2["date"].dt.to_period("M").dt.to_timestamp()
        agg = d2.groupby(["month","subject"])["score"].mean().reset_index()
        chart = (alt.Chart(agg).mark_line().encode(
            x="month:T", y="score:Q", color="subject:N", tooltip=["month:T","subject:N","score:Q"]
        ).interactive())
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No date column found; monthly chart hidden.")

    st.subheader("Download data")
    st.download_button("Export filtered scores CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="scores_export.csv", mime="text/csv")
