import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Artist Teams", layout="wide")
SideBarLinks()
st.title("👥 View PR and Marketing Teams per Artist")

API_BASE = "http://web-api:4000"

# ---------- Fetch and Display Artist Teams ----------
try:
    logger.info("Fetching artist teams...")
    response = requests.get(f"{API_BASE}/am/artist_teams")

    if response.status_code == 200:
        teams = response.json()
        if teams:
            st.success("✅ Artist teams loaded:")
            st.dataframe(teams)
        else:
            st.warning("No artist team data found.")
    else:
        st.error(f"Failed to fetch teams. Status code: {response.status_code}")
except Exception as e:
    logger.exception("Error while fetching artist team data")
    st.error(f"❌ Error fetching team info: {e}")