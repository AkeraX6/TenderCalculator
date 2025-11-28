import streamlit as st
import pandas as pd
import math
import os

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Magazine Calculator", layout="wide")

# ---------------------- HOME BUTTON ----------------------
col_home, _ = st.columns([1, 5])
with col_home:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")

# ---------------------- CSS DESIGN ----------------------
st.markdown("""
<style>

header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

div.block-container {
    padding-top: 5px !important;
    max-width: 1200px;
}

/* BUTTON STYLE */
.stButton > button {
    width: 280px !important;
    height: 70px !important;
    border-radius: 50px !important;
    border: 3px solid #E1251B !important;
    background-color: white !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #E1251B !important;
    box-shadow: 0px 6px 18px rgba(0, 0, 0, .2);
    transition: 0.18s ease-in-out !important;
}

.stButton > button:hover {
    background-color: #E1251B !important;
    color: #ffffff !important;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0px 10px 26px rgba(0, 0, 0, .3);
}

.summary-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 18px;
    border: 2px solid #E1251B25;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- LOAD PRODUCTS CSV ----------------------
df_products = pd.read_csv("data/Products_TEST.csv")

# ---------------------- SESSION INIT ----------------------
if "order" not in st.session_state:
    st.session_state.order = []

# ---------------------- PAGE TITLE ----------------------
st.markdown("<h2 style='text-align: center;'>📦 Magazine Container Calculator</h2>", unsafe_allow_html=True)

st.write("")

# ---------------------- INPUT AREA ----------------------
col1, col2, col3 = st.columns([2,1,1])

with col1:
    product = st.selectbox("Select product:", df_products["ProductName"])

with col2:
    qty = st.number_input("Quantity:", min_value=1, value=1)

with col3:
    udm = st.selectbox("Unit:", ["Boxes", "Pcs"])

# ---------------------- ADD PRODUCT BUTTON ----------------------
if st.button("➕ Add Product"):
    selected = df_products[df_products["ProductName"] == product].iloc[0]

    boxes_per_pallet = selected["BoxesPerPallet"]
    pieces_per_box = selected["PiecesPerBox"]
    pallets_per_container = selected["PalletsPerContainer"]

    # PCS→BOX conversion
    if udm == "Pcs" and pieces_per_box > 0:
        boxes = math.ceil(qty / pieces_per_box)
    else:
        boxes = qty

    pallets = math.ceil(boxes / boxes_per_pallet)
    fraction_container = pallets / pallets_per_container

    st.session_state.order.append({
        "Product": product,
        "Qty": qty,
        "Unit": udm,
        "Boxes": boxes,
        "Pallets": pallets,
        "Container Fraction": fraction_container
    })

    st.success(f"{product} added successfully ✔")

# ---------------------- ITEMS TABLE ----------------------
st.write("")
st.markdown("### Items Summary")

if len(st.session_state.order) > 0:
    order_df = pd.DataFrame(st.session_state.order)
    st.dataframe(order_df, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------- SUMMARY ----------------------
    total_containers = math.ceil(order_df["Container Fraction"].sum())

    st.markdown(f"""
    <div class="summary-box">
    <h3>🛳 Containers Required: <strong>{total_containers}</strong></h3>
    </div>
    """, unsafe_allow_html=True)

    # EXPORT EXCEL
    export_df = order_df.copy()
    export_df.to_excel("Magazine_Result.xlsx", index=False)
    with open("Magazine_Result.xlsx", "rb") as file:
        st.download_button(
            label="📤 Export to Excel",
            data=file,
            file_name="Magazine_Result.xlsx"
        )

    # CLEAR BUTTON
    if st.button("🗑 Clear All"):
        st.session_state.order = []
else:
    st.info("Add a product to start the container calculation.")


