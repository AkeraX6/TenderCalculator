import streamlit as st

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# ---------------------- GLOBAL CSS ----------------------
st.markdown("""
<style>

header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

div.block-container {
    padding-top: 0 !important; /* Remove white top space */
    margin-top: -35px !important;
    max-width: 1200px;
}

/* BUTTON STYLE */
.stButton > button {
    width: 280px !important;
    height: 95px !important;
    border-radius: 50px !important;
    border: 3px solid #E1251B !important;
    background-color: white !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #E1251B !important;
    box-shadow: 0px 6px 18px rgba(0, 0, 0, .2);
    transition: 0.18s ease-in-out !important;
}

.stButton > button:hover {
    background-color: #E1251B !important;
    color: #fff !important;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 10px 26px rgba(0, 0, 0, .3);
}

/* DESCRIPTION */
.desc {
    text-align:center; 
    font-size:18px; 
    font-style:italic;
    margin-bottom: 10px;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- BANNER ----------------------
st.image("tender_banner.png", use_column_width=True)

# ---------------------- DESCRIPTION ----------------------
st.markdown('<p class="desc">A tool to estimate requirements for mining projects.</p>', unsafe_allow_html=True)

# ---------------------- BUTTON GRID CENTERED ----------------------
# Each row is 3 columns of equal size → Perfect symmetry
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📦 Magazine"):
        st.switch_page("pages/1_Magazine.py")
with col2:
    if st.button("⚙️ Equipment"):
        st.switch_page("pages/2_Equipment.py")
with col3:
    if st.button("🏭 Plant"):
        st.switch_page("pages/3_Plant.py")

# Spacing between rows
st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("⛽ Diesel"):
        st.switch_page("pages/5_Diesel.py")
with col5:
    if st.button("👷 Personnel"):
        st.switch_page("pages/4_Personnel.py")
with col6:
    st.write("")  # Empty placeholder for symmetry
