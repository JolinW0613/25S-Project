import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title("💰 Artist Earnings and Payment Status")

artist_id = 1  # hardcoded for demo

# --------------------- Section: View Payments ---------------------
st.subheader("📄 View My Payments")

url = f"http://web-api:4000/artist/{artist_id}/payments"

try:
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data:
            st.dataframe(data)
        else:
            st.warning("No payment records found.")
    else:
        st.error(f"Failed to fetch payments. Status code: {res.status_code}")
except Exception as e:
    st.error(f"Error while fetching payments: {e}")
    logger.error(e)

# --------------------- Section: Update Payment Status ---------------------
st.subheader("✏️ Update a Payment Status")

# Two-column layout like professor's template
col1, col2 = st.columns(2)

with col1:
    payment_id = st.number_input("Enter Payment ID:", min_value=1, step=1)

with col2:
    new_status = st.selectbox("Select New Status:", ["Paid", "Pending", "Failed"])

logger.info(f'Attempting update: payment_id={payment_id}, new_status={new_status}')

if st.button("Update Payment", type="primary", use_container_width=True):
    update_url = f"http://web-api:4000/artist/{artist_id}/payment"
    payload = {"payment_id": payment_id, "payment_status": new_status}

    try:
        res = requests.put(update_url, json=payload)
        if res.status_code == 200:
            st.success("✅ Payment status updated successfully!")
        else:
            st.error(f"❌ Failed to update. Status code: {res.status_code}")
    except Exception as e:
        st.error(f"❌ Error during update: {e}")
        logger.error(e)
