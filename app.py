import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")

st.title("📊 Student Performance Analytics")
st.caption("Streamlit version — browse students, subjects, attendance, and analytics.")

# Load data
students, subjects, df = load_data()

# Sidebar global filters
with st.sidebar:
    st.header("Filters")
    # Subject filter
    subjects_list = sorted([s for s in df["subject"].dropna().unique()]) if not df.empty and "subject" in df.columns else []
    subject = st.selectbox("Subject", options=["All"] + subjects_list)
    # Performance threshold
    min_score = st.slider("Min score", 0, 100, 0)
    # Date range
    if not df.empty and "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
        min_d, max_d = df["date"].min(), df["date"].max()
        dr = st.date_input("Date range", value=(min_d, max_d))
    else:
        dr = None

def apply_filters(df):
    if df.empty:
        return df
    out = df.copy()
    if "score" in out.columns:
        out = out[out["score"].fillna(0) >= min_score]
    if subject != "All" and "subject" in out.columns:
        out = out[out["subject"] == subject]
    if dr and "date" in out.columns and pd.api.types.is_datetime64_any_dtype(out["date"]):
        start, end = pd.to_datetime(dr[0]), pd.to_datetime(dr[1])
        out = out[(out["date"] >= start) & (out["date"] <= end)]
    return out

df_f = apply_filters(df)

# Top-level KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Students", len(students))
with col2:
    avg = df_f["score"].mean() if "score" in df_f.columns and not df_f.empty else float('nan')
    st.metric("Average Score", f"{avg:.1f}%" if pd.notna(avg) else "—")
with col3:
    subjects_count = df_f["subject"].nunique() if "subject" in df_f.columns else 0
    st.metric("Active Subjects", subjects_count)
with col4:
    rows = len(df_f) if not df_f.empty else 0
    st.metric("Records", rows)

st.info("Use the sidebar to filter. Use the page selector (left bar) to explore more.")

st.dataframe(df_f.head(200))
