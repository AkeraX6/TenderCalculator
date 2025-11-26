import streamlit as st

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# Hide Streamlit default toolbar & sidebar
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# ---------------------- BANNER ----------------------
st.image("tender_banner.png", use_column_width=True)

# ---------------------- DESCRIPTION ----------------------
st.markdown(
    "<h5 style='text-align:center; font-style:italic; margin-top:10px;'>"
    "A tool to estimate requirements for mining projects."
    "</h5>",
    unsafe_allow_html=True
)

# ---------------------- BUTTON GRID ----------------------
# Create a 3x2 matrix layout of buttons
col1, col2, col3 = st.columns([1,1,1])

# === Row 1 ===
with col1:
    if st.button("📦 Magazine", use_container_width=True):
        st.switch_page("pages/1_Magazine.py")
with col2:
    if st.button("⚙️ Equipment", use_container_width=True):
        st.switch_page("pages/2_Equipment.py")
with col3:
    if st.button("🏭 Plant", use_container_width=True):
        st.switch_page("pages/3_Plant.py")

# Space between rows
st.markdown("<br>", unsafe_allow_html=True)

# === Row 2 ===
col4, col5, col6 = st.columns([1,1,1])

with col4:
    if st.button("⛽ Diesel", use_container_width=True):
        st.switch_page("pages/5_Diesel.py")
with col5:
    if st.button("👷 Personnel", use_container_width=True):
        st.switch_page("pages/4_Personnel.py")
with col6:
    st.write("")  # Empty placeholder for symmetry
