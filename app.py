
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from main_launcher import render_main_launcher

st.set_page_config(
    page_title="Future Leaders AI",
    page_icon="🧠",
    layout="wide",
)

render_main_launcher()
