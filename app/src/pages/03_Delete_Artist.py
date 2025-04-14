import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Delete Artist", layout="wide")
SideBarLinks()
st.title("🗑️ Delete Artist")

API_BASE = "http://web-api:4000"

# ---------- Input ----------
st.subheader("⚠️ Delete Artist by ID")
artist_id = st.number_input("Enter Artist ID to Delete", min_value=1, step=1)

if st.button("Delete Artist", type="primary", use_container_width=True):
    confirm = st.radio("Are you sure?", ("No", "Yes"), horizontal=True)
    
    if confirm == "Yes":
        try:
            delete_url = f"{API_BASE}/am/artist/{artist_id}"
            response = requests.delete(delete_url)

            if response.status_code == 200:
                st.success("✅ Artist successfully deleted!")
            else:
                st.error(f"❌ Failed to delete artist. Status code: {response.status_code}")
        except Exception as e:
            logger.exception("Error while deleting artist")
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Deletion cancelled. Please confirm if you're sure.")