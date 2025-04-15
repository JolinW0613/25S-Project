import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(page_title="Create Project", layout="wide")
SideBarLinks()
st.title("📁 Create New Project")

API_BASE = "http://web-api:4000"

with st.form("create_project_form"):
    name = st.text_input("Project Name", placeholder="e.g. Super Star Concert")
    project_type = st.selectbox("Project Type", ["Concert", "TV Show", "Film", "Variety Show"])
    budget = st.number_input("Budget", min_value=0.0, step=10000.0)
    revenue = st.number_input("Expected Revenue", min_value=0.0, step=10000.0)
    roi = st.number_input("ROI", min_value=0.0, step=0.1)
    approve_status = st.selectbox("Approval Status", ["Pending", "Under Review", "Approved"])
    platform_manager_id = st.number_input("Your Manager ID", step=1)
    submitted = st.form_submit_button("Create Project")

    if submitted:
        payload = {
            "name": name,
            "project_type": project_type,
            "budget": budget,
            "revenue": revenue,
            "ROI": roi,
            "approve_status": approve_status,
            "platform_manager_id": platform_manager_id
        }
        try:
            res = requests.post(f"{API_BASE}/project", json=payload)
            if res.status_code == 201:
                st.success(f"✅ Project created successfully! ID: {res.json().get('project_id')}")
            else:
                st.error(f"❌ Failed to create project. Status: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")