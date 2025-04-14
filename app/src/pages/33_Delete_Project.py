import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(page_title="Delete Project", layout="wide")
SideBarLinks()
st.title("🗑️ Delete Project")

API_BASE = "http://web-api:4000"

project_id = st.number_input("Enter Project ID to Delete", step=1)

if st.button("Delete Project", type="primary"):
    try:
        res = requests.delete(f"{API_BASE}/project/{project_id}")
        if res.status_code == 200:
            st.success("✅ Project deleted successfully.")
        elif res.status_code == 404:
            st.warning("⚠️ Project not found.")
        else:
            st.error(f"❌ Failed to delete. Status code: {res.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")