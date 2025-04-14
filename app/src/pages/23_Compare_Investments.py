import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# ---------- Page Setup ----------
st.set_page_config(page_title="Compare Investments", layout="wide")
SideBarLinks()
st.title("📊 Compare My Investments with Industry Averages")

API_BASE = "http://web-api:4000"

# ---------- Input Field ----------
investor_id = st.number_input("Enter Your Investor ID", min_value=1, step=1)

# ---------- Fetch and Display Comparison ----------
if st.button("Compare Now", type='primary', use_container_width=True):
    logger.info(f"Fetching comparison for investor_id: {investor_id}")
    url = f"{API_BASE}/invests/{investor_id}/comparisons"
    
    try:
        res = requests.get(url)
        if res.status_code == 200:
            comparison_data = res.json()
            if comparison_data:
                st.success("✅ Investment comparison loaded:")
                st.dataframe(comparison_data)
            else:
                st.warning("No comparison data found for this investor.")
        else:
            st.error(f"Failed to fetch data. Status code: {res.status_code}")
    except Exception as e:
        logger.exception("Exception occurred while fetching comparison data.")
        st.error(f"❌ Error: {e}")
