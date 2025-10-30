# Student Performance Analytics — Streamlit

This is a Streamlit version of your student analytics dashboard. It reads the CSVs you provided:
- `data/students.csv`
- `data/subjects.csv`
- `data/scores.csv`

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run app.py
```

## App structure
- `app.py`: App entry with sidebar nav and global filters.
- `pages/`: Individual pages (Dashboard, Students, Subjects, Attendance, Analytics).
- `data/`: CSV inputs.

If some CSVs are missing columns, the app will still load with best-effort fallbacks.
