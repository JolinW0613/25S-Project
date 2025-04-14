##################################################
# Home.py - Main Landing Page for the Entertainment Company Platform
##################################################

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
st.title('🎬 Star✨Flow')
st.write('\n\n')
st.write('### Welcome! Who are you logging in as?')

# Four persona login buttons - mimicking login with button clicks

if st.button("🎧 Act as Alex, an Artist Manager", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'artist_manager'
    st.session_state['first_name'] = 'Alex'
    logger.info("Logging in as Artist Manager")
    st.switch_page('pages/00_ArtistManager_Home.py')

if st.button("🎤 Act as Jamie, an Artist", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'artist'
    st.session_state['first_name'] = 'Jamie'
    logger.info("Logging in as Artist")
    st.switch_page('pages/10_Artist_Home.py')

if st.button("💼 Act as Taylor, an Investment Counsellor", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'investor'
    st.session_state['first_name'] = 'Taylor'
    logger.info("Logging in as Investment Counsellor")
    st.switch_page('pages/20_Investor_Home.py')

if st.button("🛠️ Act as Morgan, a Platform Manager", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'platform_manager'
    st.session_state['first_name'] = 'Morgan'
    logger.info("Logging in as Platform Manager")
    st.switch_page('pages/30_PlatformManager_Home.py')