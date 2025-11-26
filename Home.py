import streamlit as st

# ================= PAGE CONFIG ================= #
st.set_page_config(page_title="Tender Calculator", layout="wide")

# ================= CUSTOM CSS ================== #
st.markdown("""
<style>

/* Remove default padding & sidebar */
div.block-container {
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}

/* Background */
body {
    background-color: #F2F2F2;
}

/* Top Header Bar */
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #E1251B;
    padding: 20px;
    width: 100%;
}

/* Logo left */
.header-logo {
    position: absolute;
    left: 20px;
}

/* Title center */
.header-title {
    color: white;
    font-size: 40px;
    font-weight: 800;
    letter-spacing: 2px;
}

/* Button style */
.module-btn {
    width: 250px;
    height: 80px;
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    border-radius: 20px;
    border: none;
    color: #E1251B !important;
    background-color: white !important;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.25);
    transition: all 0.2s ease-in-out;
}

.module-btn:hover {
    background-color: #ffddd8 !important;
    transform: scale(1.05);
    cursor: pointer;
}

/* Centering Buttons */
.btn-container {
    margin-top: 80px;
    display: flex;
    justify-content: center;
    gap: 50px;
}

</style>
""", unsafe_allow_html=True)


# ================= HEADER ================= #
st.markdown(f"""
<div class="header-container">
    <img src="maxam_logo.png" class="header-logo" width="110">
    <div class="header-title">TENDER CALCULATOR</div>
</div>
""", unsafe_allow_html=True)


# ================= MAIN BUTTON GRID ================= #
st.markdown('<div class="btn-container">', unsafe_allow_html=True)

# Buttons for page navigation using session_state
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    if st.button("Magazine", key="mag"):
        st.session_state["page"] = "magazine"

with col2:
    if st.button("Equipment", key="eq"):
        st.session_state["page"] = "equipment"

with col3:
    if st.button("Plant", key="pl"):
        st.session_state["page"] = "plant"

with col4:
    if st.button("Personnel", key="per"):
        st.session_state["page"] = "personnel"

st.markdown('</div>', unsafe_allow_html=True)


# ================= NAVIGATION ENGINE ================= #
if "page" in st.session_state:
    if st.session_state["page"] == "magazine":
        st.switch_page("pages/1_Magazine.py")
    elif st.session_state["page"] == "equipment":
        st.switch_page("pages/2_Equipment.py")
    elif st.session_state["page"] == "plant":
        st.switch_page("pages/3_Plant.py")
    elif st.session_state["page"] == "personnel":
        st.switch_page("pages/4_Personnel.py")
