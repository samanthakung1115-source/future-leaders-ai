
import streamlit as st
st.set_page_config(page_title="Future Leaders AI v1.0 Release Sprint 4")
st.title("Decision Coach 2.0")
st.success("Framework Ready")
st.metric("Decision Confidence","High")
st.subheader("Today's Coaching")
for x in [
"Don't chase extended leaders",
"Review trim plan for large winners",
"Don't average down without new thesis",
"Prepare tomorrow watchlist"]:
    st.write("-",x)
