import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tender Calculator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# CUSTOM CSS (UI / THEME)
# ---------------------------------------------------------
st.markdown(
    """
<style>

/* Hide Streamlit default chrome: top bar, footer, sidebar */
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
div[data-testid="collapsedControl"] {display: none !important;}

/* Page background and container width */
body {
    background-color: #F2F2F2;
}
div.block-container {
    padding-top: 0rem;
    max-width: 1100px;
}

/* Banner */
.banner-wrapper {
    margin-left: -3rem;
    margin-right: -3rem;
}

/* Frame (card) around buttons + description */
.module-frame {
    margin-top: 2rem;
    padding: 2.5rem 3rem 2rem 3rem;
    background-color: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #DDDDDD;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

/* 2x2 grid container for buttons */
.button-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.8rem 2.8rem;
    justify-items: center;
    margin-bottom: 1.8rem;
}

/* Style ALL Streamlit buttons as pill buttons */
.stButton > button {
    width: 260px;
    height: 80px;
    border-radius: 999px;
    border: 2px solid #E1251B;
    background: #FFFFFF;
    color: #E1251B;
    font-size: 19px;
    font-weight: 600;
    letter-spacing: 0.5px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
    transition: all 0.18s ease-in-out;
}

/* Hover effect */
.stButton > button:hover {
    background: #E1251B;
    color: #FFFFFF;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0px 8px 16px rgba(0,0,0,0.22);
    cursor: pointer;
}

/* Description text inside the frame */
.tool-description {
    margin-top: 0.5rem;
    padding: 0.9rem 1.1rem;
    border-radius: 12px;
    background-color: #F7F7F7;
    border: 1px solid #E4E4E4;
    font-size: 14px;
    color: #444444;
}

/* Center alignment helper */
.center {
    text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------
st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
# Make sure "tender_banner.png" exists in the repo root
st.image("tender_banner.png", use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN FRAME (BUTTONS + DESCRIPTION)
# ---------------------------------------------------------
with st.container():
    st.markdown('<div class="module-frame">', unsafe_allow_html=True)

    # --- 2x2 button grid with icons ---
    st.markdown('<div class="button-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦  Magazine", key="mag_btn"):
            st.session_state["page"] = "magazine"
    with col2:
        if st.button("⚙️  Equipment", key="eq_btn"):
            st.session_state["page"] = "equipment"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏭  Plant", key="pl_btn"):
            st.session_state["page"] = "plant"
    with col4:
        if st.button("👷  Personnel", key="per_btn"):
            st.session_state["page"] = "personnel"

    st.markdown("</div>", unsafe_allow_html=True)  # close button-grid

    # --- Description inside small framed area ---
    st.markdown(
        """
        <div class="tool-description center">
            Tender Calculator is an internal decision-support tool that helps commercial teams
            quickly estimate magazine capacity, equipment fleet, plant requirements and
            personnel needs for new or existing projects.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close module-frame

# ---------------------------------------------------------
# NAVIGATION TO OTHER PAGES
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
