import streamlit as st

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# Hide sidebar + header + footer
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# ---------------------- CUSTOM BUTTON STYLE ----------------------
st.markdown("""
<style>

.stButton > button {
    width: 260px !important;
    height: 90px !important;
    border-radius: 50px !important;
    border: 3px solid #E1251B !important;
    background-color: white !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #E1251B !important;
    box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.18);
    transition: all .18s ease-in-out !important;
}

.stButton > button:hover {
    background-color: #E1251B !important;
    color: white !important;
    transform: translateY(-4px) scale(1.04) !important;
    box-shadow: 0px 10px 26px rgba(0, 0, 0, 0.26) !important;
}

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
# Matrix: 3 columns x 2 rows
col1, col2, col3 = st.columns([1,1,1])

# Row 1
with col1:
    if st.button("📦 Magazine"):
        st.switch_page("pages/1_Magazine.py")
with col2:
    if st.button("⚙️ Equipment"):
        st.switch_page("pages/2_Equipment.py")
with col3:
    if st.button("🏭 Plant"):
        st.switch_page("pages/3_Plant.py")

st.markdown("<br>", unsafe_allow_html=True)

# Row 2
col4, col5, col6 = st.columns([1,1,1])

with col4:
    if st.button("⛽ Diesel"):
        st.switch_page("pages/5_Diesel.py")
with col5:
    if st.button("👷 Personnel"):
        st.switch_page("pages/4_Personnel.py")
with col6:
    st.write("")  # Placeholder for symmetry
