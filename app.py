
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from ui import render_release_dashboard

st.set_page_config(
    page_title="Samantha AI Platform",
    page_icon="🧠",
    layout="wide",
)

render_release_dashboard()
