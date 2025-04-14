##################################################
# Artist - Landing Page
# File: pages/10_Artist_Home.py
##################################################

import streamlit as st
from modules.nav import SideBarLinks

# Sidebar with navigation
SideBarLinks()

# Retrieve session information
first_name = st.session_state.get('first_name', 'Artist')

# Main content
st.title(f"🎤 Welcome, {first_name} (Artist)")
st.write("This is your personalized artist dashboard. You can:")

st.markdown("""
- 📅 **View your real-time performance schedule**
- 📲 **Get updates when your schedule changes**
- 💰 **See detailed earnings breakdown per project**
- 📈 **Access insights and history for career planning**
""")

st.info("Use the sidebar to access your tools and data.")
