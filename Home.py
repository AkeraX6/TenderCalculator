import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Tender Calculator", layout="wide")

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown("""
<style>

header {visibility:hidden;}
footer {visibility:hidden;}
section[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stToolbar"] {display:none !important;}
div[data-testid="collapsedControl"] {display:none !important;}

div.block-container {
    padding-top:0rem;
    max-width:1200px;
    margin:auto;
}

.banner {
    margin-left:-4rem;
    margin-right:-4rem;
}

/* -------- BUTTON MATRIX -------- */
.button-grid {
    display:flex;
    flex-direction:column;
    align-items:center;
    margin-top:32px;
}

/* one row (horizontal) */
.button-row {
    display:flex;
    justify-content:center;
    gap:38px;
    margin-bottom:26px;
}

/* button fixed width styling */
.stButton > button {
    width:280px !important;
    height:90px !important;
    border-radius:999px !important;
    border:3px solid #E1251B !important;
    background:white !important;
    color:#E1251B !important;
    font-size:23px !important;
    font-weight:700 !important;
    letter-spacing:0.7px;
    box-shadow:0px 6px 18px rgba(0,0,0,0.20);
    transition:0.18s ease-in-out;
}

.stButton > button:hover {
    background:#E1251B !important;
    color:white !important;
    transform:translateY(-3px) scale(1.03);
    box-shadow:0px 12px 26px rgba(0,0,0,0.28);
}

/* description */
.desc {
    text-align:center;
    font-size:18px;
    font-style:italic;
    margin-top:12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------
st.markdown('<div class="banner">', unsafe_allow_html=True)
st.image("tender_banner.png", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------
st.markdown('<p class="desc">A tool to estimate requirements for mining projects.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BUTTON MATRIX (HORIZONTAL ROWS LOCKED)
# ---------------------------------------------------------
st.markdown('<div class="button-grid">', unsafe_allow_html=True)

# ROW 1
st.markdown('<div class="button-row">', unsafe_allow_html=True)
if st.button("📦 Magazine", key="mag"): st.session_state["page"] = "magazine"
if st.button("⚙️ Equipment", key="eq"): st.session_state["page"] = "equipment"
if st.button("🏭 Plant", key="pl"): st.session_state["page"] = "plant"
st.markdown('</div>', unsafe_allow_html=True)

# ROW 2
st.markdown('<div class="button-row">', unsafe_allow_html=True)
if st.button("⛽ Diesel", key="dies"): st.session_state["page"] = "diesel"
if st.button("👷 Personnel", key="per"): st.session_state["page"] = "personnel"
st.markdown('<div style="width:280px;"></div>', unsafe_allow_html=True) # placeholder
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE NAVIGATION
# ---------------------------------------------------------
if "page" in st.session_state:
    st.switch_page(
        {
            "magazine":"pages/1_Magazine.py",
            "equipment":"pages/2_Equipment.py",
            "plant":"pages/3_Plant.py",
            "diesel":"pages/5_Diesel.py",
            "personnel":"pages/4_Personnel.py",
        }[st.session_state["page"]]
    )
