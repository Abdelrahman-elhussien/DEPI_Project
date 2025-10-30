import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def _safe_read_csv(path, **kw):
    try:
        return pd.read_csv(path, **kw)
    except Exception:
        return pd.DataFrame()

def load_data():
    students = _safe_read_csv(DATA_DIR / "students.csv")
    subjects = _safe_read_csv(DATA_DIR / "subjects.csv")
    scores   = _safe_read_csv(DATA_DIR / "scores.csv", parse_dates=["date"])  # date column optional

    # Normalize column names
    def lower_cols(df):
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    students = lower_cols(students)
    subjects = lower_cols(subjects)
    scores   = lower_cols(scores)

    # Expected minimal columns (best-effort)
    # students: student_id, name (or first_name/last_name), attendance (optional), performance (optional)
    if "name" not in students.columns:
        # Try to build from first/last name
        if {"first_name", "last_name"}.issubset(students.columns):
            students["name"] = students["first_name"].astype(str) + " " + students["last_name"].astype(str)
        else:
            students["name"] = students.get("student_name", students.get("full_name", "Student"))
    if "student_id" not in students.columns:
        # Try common alternatives
        for alt in ["id", "studentid", "sid"]:
            if alt in students.columns:
                students = students.rename(columns={alt: "student_id"})
                break
        if "student_id" not in students.columns:
            students["student_id"] = range(1, len(students) + 1)

    # scores: student_id, subject, score, date
    if "student_id" not in scores.columns:
        for alt in ["id", "sid"]:
            if alt in scores.columns:
                scores = scores.rename(columns={alt: "student_id"})
                break
    if "subject" not in scores.columns:
        for alt in ["subject_name", "course", "course_name"]:
            if alt in scores.columns:
                scores = scores.rename(columns={alt: "subject"})
                break
    if "score" not in scores.columns:
        for alt in ["marks", "grade", "points"]:
            if alt in scores.columns:
                scores = scores.rename(columns={alt: "score"})
                break

    # subjects: subject, maybe subject_id, dept, etc.
    if "subject" not in subjects.columns:
        for alt in ["subject_name", "course", "course_name"]:
            if alt in subjects.columns:
                subjects = subjects.rename(columns={alt: "subject"})
                break

    # Join base table for easy use
    df = scores.copy()
    if not df.empty:
        df = df.merge(students[["student_id", "name"]], on="student_id", how="left")
        if "subject" in subjects.columns:
            df = df.merge(subjects.drop_duplicates(subset=["subject"]), on="subject", how="left")
    return students, subjects, df
