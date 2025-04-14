import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# ---------- Page Setup ----------
st.set_page_config(page_title="Artist Info & Contracts", layout="wide")
SideBarLinks()
st.title("🧾 Artist Information & Contracts")

API_BASE = "http://web-api:4000/am/artist_information"

try:
    res = requests.get(API_BASE)
    if res.status_code == 200:
        data = res.json()
        if data:
            st.success("Here is the artist information with contract details:")
            st.dataframe(data)
        else:
            st.info("No artist data found.")
    else:
        st.error(f"Failed to retrieve data. Status code: {res.status_code}")
except Exception as e:
    logger.exception("Failed to fetch artist info")
    st.error(f"❌ Error occurred: {e}")
