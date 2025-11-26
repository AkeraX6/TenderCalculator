import streamlit as st

# HOME NAVIGATION BUTTON
col_home, _ = st.columns([1, 5])
with col_home:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")

