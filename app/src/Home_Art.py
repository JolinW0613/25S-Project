import logging
import streamlit as st
from modules.nav import SideBarLinks

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Streamlit to use wide layout
st.set_page_config(layout='wide')

# Set default authentication state to False
st.session_state['authenticated'] = False

# Display the sidebar navigation (custom function)
SideBarLinks(show_home=True)

# Main page content
logger.info("Loading the Entertainment Company Home page")
st.title('🎬 Entertainment Company Internal Platform')
st.write('\n\n')
st.write('### Welcome! Who are you logging in as?')

# Four persona login buttons - mimicking login with button clicks

if st.button("🎧 Act as an Artist Manager", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'artist_manager'
    st.session_state['first_name'] = 'Artist Manager'
    logger.info("Logging in as Artist Manager")
    st.switch_page('pages/00_ArtistManager_Home.py')

if st.button("🎤 Act as an Artist", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'artist'
    st.session_state['first_name'] = 'Artist'
    logger.info("Logging in as Artist")
    st.switch_page('pages/10_Artist_Home.py')

if st.button("💼 Act as an Investment Counsellor", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'investor'
    st.session_state['first_name'] = 'Investment Counsellor'
    logger.info("Logging in as Investment Counsellor")
    st.switch_page('pages/20_Investor_Home.py')

if st.button("🛠️ Act as a Platform Manager", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'platform_manager'
    st.session_state['first_name'] = 'Platform Manager'
    logger.info("Logging in as Platform Manager")
    st.switch_page('pages/30_Platform_Home.py')
