
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from ui.service_registry_page import render

st.set_page_config(
    page_title="Future Leaders AI v1.2 Service Registry",
    page_icon="🧠",
    layout="wide",
)

render()
