import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tender Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>

header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}

body {
    background-color: #F2F2F2;
}

div.block-container {
    padding-top: 0rem;
    max-width: 1100px;
}

/* Banner edge fix */
.banner-wrapper {
    margin-left: -4rem;
    margin-right: -4rem;
}

/* Buttons container */
.buttons-section {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 26px;
}

/* Each row of buttons */
.button-row {
    display: flex;
    justify-content: center;
    gap: 28px;
}

/* Pill button styling */
.stButton > button {
    width: 300px;
    height: 95px;
    border-radius: 999px;
    border: 3px solid #E1251B;
    background: #FFFFFF;
    color: #E1251B;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.8px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.16);
    transition: all 0.18s ease-in-out;
}

/* Hover effect */
.stButton > button:hover {
    background: #E1251B;
    color: #FFFFFF;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 12px 26px rgba(0,0,0,0.26);
    cursor: pointer;
}

/* Description card */
.description-box {
    margin: 1.2rem auto 1.1rem auto;
    padding: 0.8rem 1.3rem;
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #DDDDDD;
    text-align: center;
    font-size: 16px;
    color: #333333;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------
st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
st.image("tender_banner.png", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------
st.markdown("""
<div class="description-box">
Tender Calculator is a decision-support tool that helps commercial teams quickly 
estimate magazine capacity, equipment fleet, plant requirements, and personnel 
needs for new or existing mining projects.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BUTTONS SECTION
# ---------------------------------------------------------
st.markdown('<div class="buttons-section">', unsafe_allow_html=True)

# --- Row 1 ---
st.markdown('<div class="button-row">', unsafe_allow_html=True)
if st.button("📦 Magazine", key="mag"): st.session_state["page"] = "magazine"
if st.button("⚙️ Equipment", key="eq"): st.session_state["page"] = "equipment"
st.markdown('</div>', unsafe_allow_html=True)

# --- Row 2 ---
st.markdown('<div class="button-row">', unsafe_allow_html=True)
if st.button("🏭 Plant", key="pl"): st.session_state["page"] = "plant"
if st.button("👷 Personnel", key="per"): st.session_state["page"] = "personnel"
st.markdown('</div>', unsafe_allow_html=True)

# --- Row 3 (Diesel centered) ---
st.markdown('<div class="button-row">', unsafe_allow_html=True)
if st.button("⛽ Diesel", key="dies"): st.session_state["page"] = "diesel"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE NAVIGATION
# ---------------------------------------------------------
if "page" in st.session_state:
    if st.session_state["page"] == "magazine":
        st.switch_page("pages/1_Magazine.py")
    elif st.session_state["page"] == "equipment":
        st.switch_page("pages/2_Equipment.py")
    elif st.session_state["page"] == "plant":
        st.switch_page("pages/3_Plant.py")
    elif st.session_state["page"] == "personnel":
        st.switch_page("pages/4_Personnel.py")
    elif st.session_state["page"] == "diesel":
        st.switch_page("pages/5_Diesel.py")
