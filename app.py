
import streamlit as st
st.set_page_config(page_title="Future Leaders AI v1.0 Release Sprint 3")
st.title("Future Leaders AI v1.0 Release - Sprint 3")
st.success("STS Portfolio Integration Framework")
st.metric("Portfolio Health Score","92")
st.subheader("Modules")
for m in [
"Portfolio Import",
"Health Score",
"Add Candidates",
"Trim Candidates",
"Risk Alerts",
"Cross Analysis"]:
    st.write("-",m)
