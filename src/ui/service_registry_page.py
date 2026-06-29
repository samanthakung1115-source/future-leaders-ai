
import streamlit as st

from service_registry import get_registry


def render():
    st.title("Service Registry")
    st.caption("Future Leaders AI v1.2 RC Sprint 2")

    registry = get_registry()
    statuses = [s.to_dict() for s in registry.all_status()]

    ok_count = sum(1 for s in statuses if s["available"])
    total = len(statuses)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Services", total)
    with c2:
        st.metric("Available", ok_count)
    with c3:
        st.metric("Missing", total - ok_count)

    st.divider()

    for item in statuses:
        with st.container(border=True):
            if item["available"]:
                st.success(f"{item['name']} — {item['module']}.{item['attribute']}")
            else:
                st.warning(f"{item['name']} — missing")
                st.caption(item["message"])

    with st.expander("Raw status"):
        st.json(statuses)
