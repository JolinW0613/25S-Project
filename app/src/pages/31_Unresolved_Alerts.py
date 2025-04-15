import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Unresolved Alerts", layout="wide")
SideBarLinks()
st.title("🚨 Unresolved Alerts")

API_BASE = "http://web-api:4000"

# ---------- Fetch Alert Data ----------
st.subheader("📡 All Unresolved Alerts")

if st.button("🔄 Refresh Alert List", type="primary", use_container_width=True):
    try:
        response = requests.get(f"{API_BASE}/pm/alerts")
        logger.info(f"GET {API_BASE}/pm/alerts → Status: {response.status_code}")

        if response.status_code == 200:
            alerts = response.json()
            if alerts:
                st.success("📋 Unresolved alerts loaded successfully.")
                st.dataframe(alerts)
            else:
                st.warning("🎉 No unresolved alerts found!")
        else:
            st.error(f"Failed to fetch alerts. Status code: {response.status_code}")
    except Exception as e:
        logger.exception("Error retrieving unresolved alerts")
        st.error(f"❌ Error fetching alerts: {e}")