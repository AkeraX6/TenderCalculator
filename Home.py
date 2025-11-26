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

/* Hide unwanted Streamlit UI */
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}

/* Page layout */
div.block-container {
    padding-top: 0rem;
    max-width: 1050px;
}

/* Banner width fix */
.banner-wrapper {
    margin-left: -3.5rem;
    margin-right: -3.5rem;
}

/* Container grouping */
.buttons-section {
    margin-top: 1.6rem;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 55px;
}

/* Two column structure */
.col-left, .col-right {
    display: flex;
    flex-direction: column;
    gap: 22px;
    align-items: center;
}

/* Button Style */
.stButton > button {
    width: 270px;
    height: 90px;
    border-radius: 999px;
    border: 3px solid #E1251B;
    background: #FFFFFF;
    color: #E1251B;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: 0.7px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.16);
    transition: all 0.18s ease-in-out;
}

/* Hover animation */
.stButton > button:hover {
    background: #E1251B;
    color: white;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 12px 28px rgba(0,0,0,0.26);
}

/* Italic description */
.description-box {
    margin-top: 1.0rem;
    text-align: center;
    font-size: 18px;
    font-style: italic;
    color: #333;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------
st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
st.image("tender_banner.png", use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SHORT DESCRIPTION (ITALIC)
# ---------------------------------------------------------
st.markdown("""
<div class="description-box">
A fast support tool for commercial teams to estimate requirements for new mining projects.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BUTTON GRID (5 BUTTONS, 2 COLUMNS)
# ---------------------------------------------------------
st.markdown('<div class="buttons-section">', unsafe_allow_html=True)

# LEFT COLUMN (3 buttons)
st.markdown('<div class="col-left">', unsafe_allow_html=True)
if st.button("📦 Magazine", key="mag"): st.session_state["page"] = "magazine"
if st.button("⚙️ Equipment", key="eq"): st.session_state["page"] = "equipment"
if st.button("🏭 Plant", key="pl"): st.session_state["page"] = "plant"
st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN (2 buttons)
st.markdown('<div class="col-right">', unsafe_allow_html=True)
if st.button("⛽ Diesel", key="dies"): st.session_state["page"] = "diesel"
if st.button("👷 Personnel", key="per"): st.session_state["page"] = "personnel"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

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
