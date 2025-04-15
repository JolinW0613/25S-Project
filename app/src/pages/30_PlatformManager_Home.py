##################################################
# Platform Manager - Landing Page
# File: pages/30_Platform_Home.py
##################################################

import streamlit as st
from modules.nav import SideBarLinks

# Sidebar
SideBarLinks()

# Session info
first_name = st.session_state.get('first_name', 'Platform Manager')

# Content
st.title(f"🛠️ Welcome, {first_name} (Platform Manager)")
st.write("Monitor system status and manage user access:")

st.markdown("""
- 🔐 **Assign role-based access to sensitive data**
- 🧩 **Ensure platform stability during high-traffic events**
- 📡 **Review user-generated content for policy compliance**
- 🛠️ **Respond to technical issues and integrate real-time data**
""")

st.info("Access platform tools and admin controls via the sidebar.")