##################################################
# Investment Counsellor - Landing Page
# File: pages/20_Investor_Home.py
##################################################

import streamlit as st
from modules.nav import SideBarLinks

# Sidebar
SideBarLinks()

# Session data
first_name = st.session_state.get('first_name', 'Investor')

# Page content
st.title(f"💼 Welcome, {first_name} (Investment Counsellor)")
st.write("Track, evaluate, and strategize your investments:")

st.markdown("""
- 📊 **Explore current entertainment projects open for investment**
- 🧾 **Monitor financial performance and audience reception**
- ⚠️ **Get real-time alerts for critical project changes**
- 🧠 **Analyze trends and risks to make smarter decisions**
""")

st.info("Choose an option from the sidebar to continue.")