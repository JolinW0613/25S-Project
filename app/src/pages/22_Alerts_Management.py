import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Alert Management", layout="wide")
SideBarLinks()
st.title("🔔 Alert Management")

API_BASE = "http://web-api:4000/in"

# ---------- Section 1: Create Alert ----------
st.subheader("📌 Create New Alert")

with st.form("create_alert_form"):
    project_id = st.number_input("Project ID", min_value=1, step=1)
    alert_type = st.text_input("Alert Type (e.g., Delay, Budget Issue)")
    alert_time = st.text_input("Alert Time (e.g., 2025-04-15 10:00:00)")
    
    submitted = st.form_submit_button("Create Alert", type='primary', use_container_width=True)
    if submitted:
        logger.info(f"Creating alert for project {project_id}")
        payload = {
            "project_id": project_id,
            "alert_type": alert_type,
            "alert_time": alert_time,
            "is_resolved": False
        }
        try:
            res = requests.post(f"{API_BASE}/alerts", json=payload)
            if res.status_code == 201:
                st.success(f"✅ Alert created! ID: {res.json().get('alert_id')}")
            else:
                st.error(f"Failed to create alert. Code: {res.status_code}")
        except Exception as e:
            logger.exception("Error creating alert")
            st.error(f"❌ Error: {e}")

# ---------- Section 2: Update Alert ----------
st.subheader("✅ Mark Alert as Resolved")

with st.form("update_alert_form"):
    update_id = st.number_input("Alert ID", step=1)
    update_btn = st.form_submit_button("Mark Resolved", type='primary', use_container_width=True)
    if update_btn:
        logger.info(f"Resolving alert ID: {update_id}")
        try:
            res = requests.put(f"{API_BASE}/alerts/{update_id}", json={"is_resolved": True})
            if res.status_code == 200:
                st.success("✅ Alert marked as resolved.")
            else:
                st.error(f"Failed to update alert. Code: {res.status_code}")
        except Exception as e:
            logger.exception("Error updating alert")
            st.error(f"❌ Error: {e}")

# ---------- Section 3: Delete Alert ----------
st.subheader("❌ Delete Alert")

with st.form("delete_alert_form"):
    delete_id = st.number_input("Alert ID", step=1, key="delete")
    delete_btn = st.form_submit_button("Delete Alert", type='primary', use_container_width=True)
    if delete_btn:
        logger.info(f"Deleting alert ID: {delete_id}")
        try:
            res = requests.delete(f"{API_BASE}/alerts/{delete_id}")
            if res.status_code == 200:
                st.success("🗑️ Alert deleted.")
            else:
                st.error(f"Failed to delete alert. Code: {res.status_code}")
        except Exception as e:
            logger.exception("Error deleting alert")
            st.error(f"❌ Error: {e}")