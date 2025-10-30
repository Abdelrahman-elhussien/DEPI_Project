import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
st.title("🏠 Dashboard")

students, subjects, df = load_data()

if df.empty:
    st.warning("No score data found. Please ensure `data/scores.csv` exists.")
else:
    left, right = st.columns(2)
    with left:
        st.subheader("Average score trend")
        if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
            ts = df.copy()
            ts["month"] = ts["date"].dt.to_period("M").dt.to_timestamp()
            chart = (alt.Chart(ts)
                        .mark_line(point=True)
                        .encode(x="month:T", y=alt.Y("mean(score):Q", title="Avg score"), tooltip=["month:T", alt.Tooltip("mean(score):Q", format=".1f")])
                        .interactive())
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No valid dates in scores; trend chart hidden.")

    with right:
        st.subheader("Performance distribution")
        bins = alt.Bin(maxbins=20)
        chart = (alt.Chart(df)
                   .mark_bar()
                   .encode(x=alt.X("score:Q", bin=bins), y="count()", tooltip=[alt.Tooltip("count():Q", title="Students")])
                   .interactive())
        st.altair_chart(chart, use_container_width=True)

    st.subheader("Recent records")
    st.dataframe(df.sort_values(df["date"] if "date" in df.columns else df.index, ascending=False).head(50))
