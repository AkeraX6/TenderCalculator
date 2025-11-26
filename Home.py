# ---------------------------------------------------------
# BUTTON GRID (finally fixed)
# ---------------------------------------------------------

st.markdown("""
<div class="button-grid">
    <div class="button-row">
        <div class="btn-wrapper">""" , unsafe_allow_html=True)
if st.button("📦 Magazine", key="mag"): st.session_state["page"] = "magazine"
st.markdown("""
        </div>
        <div class="btn-wrapper">""", unsafe_allow_html=True)
if st.button("⚙️ Equipment", key="eq"): st.session_state["page"] = "equipment"
st.markdown("""
        </div>
        <div class="btn-wrapper">""", unsafe_allow_html=True)
if st.button("🏭 Plant", key="pl"): st.session_state["page"] = "plant"
st.markdown("""
        </div>
    </div>
    <div class="button-row">
        <div class="btn-wrapper">""", unsafe_allow_html=True)
if st.button("⛽ Diesel", key="dies"): st.session_state["page"] = "diesel"
st.markdown("""
        </div>
        <div class="btn-wrapper">""", unsafe_allow_html=True)
if st.button("👷 Personnel", key="per"): st.session_state["page"] = "personnel"
st.markdown("""
        </div>
        <div class="btn-wrapper"></div> <!-- placeholder -->
    </div>
</div>
""", unsafe_allow_html=True)
