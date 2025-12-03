import streamlit as st

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# ---------------------- THEME TOGGLE ----------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Place toggle on top right
top_right = st.columns([10, 1])[1]
with top_right:
    theme_choice = st.toggle("🌙", help="Toggle dark mode", value=(st.session_state.theme == "dark"))

if theme_choice:
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"


# ---------------------- GLOBAL CSS BASE ----------------------
base_css = """
<style>

header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

div.block-container {
    padding-top: 0 !important;
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
"""
st.markdown(base_css, unsafe_allow_html=True)


# ---------------------- DARK MODE OVERRIDE ----------------------
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    body, .stApp, .block-container {
        background-color: #121212 !important;
        color: #E0E0E0 !important;
    }

    .desc {
        color: #C8C8C8 !important;
    }

    /* Dark mode buttons */
    .stButton > button {
        background-color: #1E1E1E !important;
        color: #E1251B !important;
        border: 3px solid #E1251B !important;
    }

    .stButton > button:hover {
        background-color: #E1251B !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------- BANNER ----------------------
st.image("tender_banner.png", use_column_width=True)

# ---------------------- DESCRIPTION ----------------------
st.markdown('<p class="desc">A tool to estimate requirements for mining projects.</p>', unsafe_allow_html=True)

# ---------------------- BUTTON GRID CENTERED ----------------------
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
    st.write("")  # Symmetry placeholder
