
import io
import csv
import streamlit as st

from sts_live import STSLiveReader
from product.samantha_daily_product import SamanthaDailyProduct


SAMPLE_CANDIDATES = [
    {"ticker": "TEM", "score": 82, "why_selected": "AI healthcare platform"},
    {"ticker": "RKLB", "score": 88, "why_selected": "Space infrastructure execution"},
    {"ticker": "MRVL", "score": 76, "why_selected": "AI infrastructure custom silicon"},
]


def render():
    st.title("Samantha AI - STS Live Integration")
    st.caption("Future Leaders AI v11 Beta 10")

    uploaded = st.file_uploader("Upload STS CSV", type=["csv"])

    if uploaded:
        text = uploaded.getvalue().decode("utf-8-sig")
        positions = STSLiveReader().load_file(io.StringIO(text))
    else:
        st.info("No file uploaded. Using sample STS portfolio.")
        positions = STSLiveReader().load_path("data/samples/sts_live_sample.csv")

    product = SamanthaDailyProduct()
    result = product.build(positions, SAMPLE_CANDIDATES)

    st.subheader("Samantha Comment")
    st.write(result["samantha_comment"])

    st.subheader("Portfolio Brief")
    st.json(result["portfolio"])

    st.subheader("Future Leaders")
    for c in result["future_leaders"]:
        st.write(f"{c['ticker']} — Score {c['score']} — {c.get('why_selected','')}")
