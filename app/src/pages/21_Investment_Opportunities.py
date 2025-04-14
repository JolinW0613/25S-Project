import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(page_title="Investment Opportunities", layout="wide")
SideBarLinks()

st.title("💼 Investment Opportunities")

# ------------------- Fetch Project Opportunities -------------------
st.subheader("🔎 Projects Open for Investment")

url = "http://web-api:4000/in/projects/opportunities"

try:
    logger.info(f"Sending GET request to {url}")
    response = requests.get(url)
    if response.status_code == 200:
        projects = response.json()
        if projects:
            st.success("✅ Current investment-ready projects:")
            st.dataframe(projects)
        else:
            st.warning("No open projects at the moment.")
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        logger.error(f"Bad status code {response.status_code} from API.")
except Exception as e:
    st.error(f"Error retrieving project opportunities: {e}")
    logger.exception("Exception during project fetch")