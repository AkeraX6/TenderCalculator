import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# -------------------------------------------------
# THEME STATE & TOGGLE CSS
# -------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Make toggle fixed at top-right corner
st.markdown("""
<style>
#theme-toggle {
    position: fixed;
    top: 12px;
    right: 22px;
    z-index: 9999;
}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Render toggle
with st.container():
    st.markdown('<div id="theme-toggle"></div>', unsafe_allow_html=True)
    toggle = st.toggle("🌙", value=(st.session_state.theme == "dark"), help="Toggle Dark Mode")

st.session_state.theme = "dark" if toggle else "light"

# -------------------------------------------------
# LIGHT & DARK MODE STYLES
# -------------------------------------------------
light_css = """
<style>
div.block-container {
    padding-top: 0 !important;
    margin-top: -35px !important;
    max-width: 1200px;
}
.stApp {
    background-color: #ffffff !important;
    color: #000000 !important;
}
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
    transition: 0.18s !important;
}
.stButton > button:hover {
    background-color: #E1251B !important;
    color: #ffffff !important;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 10px 26px rgba(0, 0, 0, .3);
}
.desc {
    text-align:center;
    font-size:18px;
    font-style:italic;
    margin-bottom:10px;
    margin-top:8px;
}
</style>
"""

dark_css = """
<style>
div.block-container {
    padding-top: 0 !important;
    margin-top: -35px !important;
    max-width: 1200px;
}
.stApp {
    background-color: #121212 !important;
    color: #E0E0E0 !important;
}
.desc {
    color: #C8C8C8 !important;
}
.stButton > button {
    background-color: #1E1E1E !important;
    color: #E1251B !important;
    border: 3px solid #E1251B !important;
    width: 280px !important;
    height: 95px !important;
    border-radius: 50px !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    box-shadow: 0px 6px 18px rgba(255, 255, 255, .1);
    transition: 0.18s !important;
}
.stButton > button:hover {
    background-color: #E1251B !important;
    color: #ffffff !important;
    transform: translateY(-3px) scale(1.03);
}
</style>
"""

if st.session_state.theme == "dark":
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)

# -------------------------------------------------
# BANNER
# -------------------------------------------------
st.image("tender_banner.png", use_column_width=True)

# -------------------------------------------------
# DESCRIPTION
# -------------------------------------------------
st.markdown('<p class="desc">A tool to estimate requirements for mining projects.</p>',
            unsafe_allow_html=True)

# -------------------------------------------------
# BUTTON GRID
# -------------------------------------------------
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

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("⛽ Diesel"):
        st.switch_page("pages/5_Diesel.py")
with col5:
    if st.button("👷 Personnel"):
        st.switch_page("pages/4_Personnel.py")
with col6:
    st.write("")  # symmetry

