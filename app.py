
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
import streamlit as st
from news_watch import NewsWatchEngine

st.set_page_config(page_title="Release Sprint 6")
st.title("News Watch Architecture")
e=NewsWatchEngine()
st.success(e.summary()["status"])
st.subheader("Planned Providers")
for p in e.providers():
    st.write("-",p)
st.subheader("Tracked Categories")
for c in e.categories():
    st.write("-",c)
st.info(e.summary()["next_step"])
