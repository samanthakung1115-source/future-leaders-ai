
import streamlit as st

st.set_page_config(page_title="Future Leaders AI v1.0 Release", layout="wide")
st.title("Future Leaders AI v1.0 Release")
st.success("Release Final")

modules=[
"Dashboard",
"Future Leaders Ranking Engine",
"STS Portfolio Integration",
"Decision Coach 2.0",
"Daily Report & Export Center",
"News Watch"
]

st.subheader("Integrated Modules")
for m in modules:
    st.write("✅",m)

st.info("Next version: v1.1")
