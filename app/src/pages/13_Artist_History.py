import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title("📜 Past Performances and Earnings")

# ------------------- Input: Select Artist and Cutoff Date -------------------
artist_id = 1  # Demo artist, hardcoded for now

st.subheader("📅 View Historical Performances")

col1, col2 = st.columns(2)

with col1:
    cutoff_date = st.date_input("Cutoff Date", help="Only show performances before this date.")

with col2:
    st.write("Click the button to fetch performance history.")

# ------------------- Fetch and Display History -------------------
if cutoff_date and st.button("Show History", type="primary", use_container_width=True):
    url = f"http://web-api:4000/artist/{artist_id}/history?cutoff={cutoff_date}"
    logger.info(f"Fetching performance history for artist {artist_id} before {cutoff_date}")
    
    try:
        res = requests.get(url)
        if res.status_code == 200:
            history = res.json()
            if history:
                st.success("✅ Performance history retrieved:")
                st.dataframe(history)
            else:
                st.warning("No historical performances found.")
        else:
            st.error(f"Failed to load history. Status code: {res.status_code}")
            logger.error(f"API returned status {res.status_code}")
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        logger.exception("Exception during history fetch")
