import streamlit as st
import requests
from modules.nav import SideBarLinks

# Page setup
st.set_page_config(page_title="Artist Schedule", layout="wide")
st.title("📅 Artist Performance Schedule")

# Sidebar nav
SideBarLinks()

# API call to get artist schedule
try:
    res = requests.get("http://web-api:4000/am/artist_schedule")

    if res.status_code == 200:
        schedule = res.json()
        if schedule:
            st.success("Here is the current schedule of all artists:")
            st.dataframe(schedule)
        else:
            st.warning("No upcoming performances found.")
    else:
        st.error(f"Failed to load artist schedule. Status code: {res.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Error connecting to API: {e}")