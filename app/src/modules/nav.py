import streamlit as st

# ------------------- Navigation Functions -------------------

def HomeNav():
    st.sidebar.page_link("Home.py", label="🏠 Home")

def ArtistManagerNav():
    st.sidebar.page_link("pages/00_ArtistManager_Home.py", label="🎧 Artist Manager", icon="🎧")
    st.sidebar.page_link("pages/01_Artist_info.py", label="🧾 View Artist Info")
    st.sidebar.page_link("pages/02_Artist_Teams.py", label="👥 View Artist Teams")
    st.sidebar.page_link("pages/03_Delete_Artist.py", label="🗑️ Delete Artist")

def ArtistNav():
    st.sidebar.page_link("pages/10_Artist_Home.py", label="🎤 Artist", icon="🎤")
    st.sidebar.page_link("pages/11_Artist_Schedule.py", label="📅 View Schedule")
    st.sidebar.page_link("pages/12_Artist_Payments.py", label="💰 Payments")
    st.sidebar.page_link("pages/13_Artist_History.py", label="📚 Performance History")

def InvestorNav():
    st.sidebar.page_link("pages/20_Investor_Home.py", label="💼 Investment Counsellor", icon="💼")
    st.sidebar.page_link("pages/21_Investment_Opportunities.py", label="📂 View Opportunities")
    st.sidebar.page_link("pages/22_Alerts_Management.py", label="🔔 Manage Alerts")
    st.sidebar.page_link("pages/23_Compare_Investments.py", label="📊 Compare with Industry")

def PlatformManagerNav():
    st.sidebar.page_link("pages/30_PlatformManager_Home.py", label="🛠️ Platform Manager", icon="🛠️")
    st.sidebar.page_link("pages/31_Unresolved_Alerts.py", label="🚨 Unresolved Alerts")
    st.sidebar.page_link("pages/32_Create_Project.py", label="➕ Create Project")
    st.sidebar.page_link("pages/33_Delete_Project.py", label="🗑️ Delete Project")

# ------------------- Sidebar Links Controller -------------------

def SideBarLinks(show_home=False):
    st.sidebar.image("assets/logo.png", width=150)

    # Redirect to home if not authenticated
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        HomeNav()

    # Show role-based pages
    if st.session_state["authenticated"]:
        role = st.session_state["role"]

        if role == "artist_manager":
            ArtistManagerNav()

        elif role == "artist":
            ArtistNav()

        elif role == "investor":
            InvestorNav()

        elif role == "platform_manager":
            PlatformManagerNav()

        # Logout button
        if st.sidebar.button("🚪 Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")