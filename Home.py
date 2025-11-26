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
# CSS
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
    margin: auto;
}

/* Banner push to sides */
.banner-wrapper {
    margin-left: -4rem;
    margin-right: -4rem;
}

/* Button Grid */
.button-grid {
    margin-top: 2.2rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    justify-items: center;
    row-gap: 28px;
}

/* Button Style */
.stButton > button {
    width: 270px;
    height: 95px;
    border-radius: 999px;
    border: 3px solid #E1251B;
    background: #fff;
    color: #E1251B;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.8px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.18);
    transition: all 0.18s ease-in-out;
}

/* Hover effect */
.stButton > button:hover {
    background: #E1251B;
    color: #fff;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 12px 26px rgba(0,0,0,0.28);
}

/* Italic description */
.description-box {
    margin-top: 1rem;
    text-align: center;
    font-size: 18px;
    font-style: italic;
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
# SHORT DESCRIPTION
# ---------------------------------------------------------
st.markdown('<div class="description-box">A tool to estimate requirements for mining projects.</div>',
            unsafe_allow_html=True)

# ---------------------------------------------------------
# BUTTON GRID (3x3 layout)
# ---------------------------------------------------------
st.markdown('<div class="button-grid">', unsafe_allow_html=True)

# Row 1
if st.button("📦 Magazine", key="mag"): st.session_state["page"] = "magazine"
if st.button("⚙️ Equipment", key="eq"): st.session_state["page"] = "equipment"
if st.button("🏭 Plant", key="pl"): st.session_state["page"] = "plant"

# Row 2
if st.button("⛽ Diesel", key="dies"): st.session_state["page"] = "diesel"
if st.button("👷 Personnel", key="per"): st.session_state["page"] = "personnel"
st.markdown("<div></div>", unsafe_allow_html=True) # Placeholder to preserve grid

# Row 3 -> all placeholders for now, to complete the 3x3 design
st.markdown("<div></div>", unsafe_allow_html=True)
st.markdown("<div></div>", unsafe_allow_html=True)
st.markdown("<div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------
if "page" in st.session_state:
    if st.session_state["page"] == "magazine":
        st.switch_page("pages/1_Magazine.py")
    elif st.session_state["page"] == "equipment":
        st.switch_page("pages/2_Equipment.py")
    elif st.session_state["page"] == "plant":
        st.switch_page("pages/3_Plant.py")
    elif st.session_state["page"] == "diesel":
        st.switch_page("pages/5_Diesel.py")
    elif st.session_state["page"] == "personnel":
        st.switch_page("pages/4_Personnel.py")
