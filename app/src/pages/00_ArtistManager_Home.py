##################################################
# Artist Manager - Landing Page
# File: pages/00_ArtistManager_Home.py
##################################################

import streamlit as st
from modules.nav import SideBarLinks

# Set up the sidebar for navigation (shows current user and page links)
SideBarLinks()

# Retrieve session information
first_name = st.session_state.get('first_name', 'Manager')

# Main content for the artist manager
st.title(f"🎧 Welcome, {first_name} (Artist Manager)")
st.write("This is your personalized dashboard. From here, you can:")

# List of features available to the Artist Manager persona
st.markdown("""
- 📅 **View and manage artists' performance schedules**
- 🧾 **Access artist contract terms and revenue breakdown**
- 💬 **Message artists for updates or emergencies**
- 🧑‍🤝‍🧑 **View PR and marketing teams per artist**
- 💰 **Track revenue distribution and ensure fair payments**
""")

st.info("Use the sidebar to navigate between features.")
