import streamlit as st
import pandas as pd
import math
from io import BytesIO

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

/* Main title */
h2 {
    text-align: center;
}

/* Buttons (global style) */
.stButton > button {
    border-radius: 40px !important;
    border: 3px solid #E1251B !important;
    background-color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #E1251B !important;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, .18);
    transition: 0.18s ease-in-out !important;
}
.stButton > button:hover {
    background-color: #E1251B !important;
    color: #ffffff !important;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0px 9px 20px rgba(0, 0, 0, .28);
}

.product-row {
    padding: 6px 10px;
    border-radius: 10px;
    background-color: #F7F7F7;
    margin-bottom: 6px;
    border: 1px solid #E0E0E0;
}

.summary-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 18px;
    border: 2px solid #E1251B25;
    text-align: center;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- LOAD PRODUCTS CSV ----------------------
@st.cache_data
def load_products():
    return pd.read_csv("data/Products_TEST.csv")

df_products = load_products()

# Ensure correct columns exist
required_cols = {"ProductName", "BoxesPerPallet", "PiecesPerBox", "PalletsPerContainer"}
missing = required_cols - set(df_products.columns)
if missing:
    st.error(f"Missing columns in Products_TEST.csv: {missing}")
    st.stop()

# ---------------------- SESSION INIT ----------------------
if "mag_order" not in st.session_state:
    st.session_state.mag_order = []  # list of dicts
if "mag_calc_result" not in st.session_state:
    st.session_state.mag_calc_result = None
if "mag_calc_table" not in st.session_state:
    st.session_state.mag_calc_table = None

# ---------------------- PAGE TITLE ----------------------
st.markdown("## 📦 Magazine Container Calculator")
st.markdown(
    "<p style='text-align:center;font-style:italic;'>"
    "Add requested products, then click <strong>Calculate</strong> to estimate container needs."
    "</p>",
    unsafe_allow_html=True
)

st.write("")

# ---------------------- ADD PRODUCT AREA ----------------------
st.markdown("### ➕ Add Product")

add_col1, add_col2, add_col3, add_col4 = st.columns([3, 1.5, 1.5, 1])

with add_col1:
    new_product = st.selectbox("Product", df_products["ProductName"], key="new_product")

with add_col2:
    new_qty = st.number_input("Quantity", min_value=1, value=1, key="new_qty")

with add_col3:
    new_unit = st.selectbox("UDM", ["Boxes", "Pcs"], key="new_unit")

with add_col4:
    if st.button("Add", key="add_row"):
        st.session_state.mag_order.append(
            {
                "Product": new_product,
                "Qty": new_qty,
                "Unit": new_unit
            }
        )
        st.session_state.mag_calc_result = None
        st.session_state.mag_calc_table = None
        st.success(f"{new_product} added.")


# ---------------------- EXISTING PRODUCTS LIST ----------------------
st.markdown("### 🧾 Product List")

if len(st.session_state.mag_order) == 0:
    st.info("No products added yet. Use the 'Add' button above to add items.")
else:
    # Display each row as editable line
    for i, row in enumerate(st.session_state.mag_order):
        with st.container():
            st.markdown("<div class='product-row'>", unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])

            with c1:
                prod_key = f"prod_{i}"
                current_prod = st.selectbox(
                    "Product",
                    df_products["ProductName"],
                    index=df_products[df_products["ProductName"] == row["Product"]].index[0]
                    if row["Product"] in df_products["ProductName"].values else 0,
                    key=prod_key
                )

            with c2:
                qty_key = f"qty_{i}"
                current_qty = st.number_input(
                    "Qty",
                    min_value=1,
                    value=int(row["Qty"]),
                    key=qty_key
                )

            with c3:
                udm_key = f"unit_{i}"
                current_unit = st.selectbox(
                    "UDM",
                    ["Boxes", "Pcs"],
                    index=0 if row["Unit"] == "Boxes" else 1,
                    key=udm_key
                )

            with c4:
                if st.button("✏ Update", key=f"update_{i}"):
                    row["Product"] = current_prod
                    row["Qty"] = current_qty
                    row["Unit"] = current_unit
                    st.session_state.mag_calc_result = None
                    st.session_state.mag_calc_table = None
                    st.success(f"Row {i+1} updated.")

            with c5:
                if st.button("🗑 Delete", key=f"del_{i}"):
                    st.session_state.mag_order.pop(i)
                    st.session_state.mag_calc_result = None
                    st.session_state.mag_calc_table = None
                    st.warning(f"Row {i+1} deleted.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.stop()  # Stop to avoid index mismatch

            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🗑 Clear All Products"):
        st.session_state.mag_order = []
        st.session_state.mag_calc_result = None
        st.session_state.mag_calc_table = None
        st.warning("All products cleared.")


# ---------------------- CALCULATION LOGIC ----------------------
def calculate_containers(order_rows, df_ref):
    results = []
    total_fraction = 0.0

    for row in order_rows:
        prod_name = row["Product"]
        qty = row["Qty"]
        unit = row["Unit"]

        prod_data = df_ref[df_ref["ProductName"] == prod_name]
        if prod_data.empty:
            continue

        boxes_per_pallet = prod_data["BoxesPerPallet"].iloc[0]
        pieces_per_box = prod_data["PiecesPerBox"].iloc[0]
        pallets_per_container = prod_data["PalletsPerContainer"].iloc[0]

        # Safety defaults
        if not isinstance(pallets_per_container, (int, float)) or pallets_per_container <= 0:
            pallets_per_container = 20

        # Convert qty to boxes
        if unit == "Pcs" and pieces_per_box and pieces_per_box > 0:
            boxes = math.ceil(qty / pieces_per_box)
        else:
            boxes = qty  # already in boxes

        pallets = math.ceil(boxes / boxes_per_pallet) if boxes_per_pallet > 0 else 0
        fraction = pallets / pallets_per_container if pallets_per_container > 0 else 0

        total_fraction += fraction

        results.append({
            "Product": prod_name,
            "Qty entered": qty,
            "Unit": unit,
            "Boxes (calculated)": boxes,
            "Pallets": pallets,
            "Container fraction": round(fraction, 3)
        })

    total_containers = math.ceil(total_fraction)

    return results, total_fraction, total_containers


st.write("")
st.markdown("---")

# ---------------------- CALCULATE BUTTON ----------------------
if len(st.session_state.mag_order) > 0:
    if st.button("🛳 Calculate Containers"):
        table, total_fraction, total_containers = calculate_containers(
            st.session_state.mag_order, df_products
        )
        st.session_state.mag_calc_table = pd.DataFrame(table)
        st.session_state.mag_calc_result = {
            "total_fraction": total_fraction,
            "total_containers": total_containers
        }

# ---------------------- SHOW RESULTS ----------------------
if st.session_state.mag_calc_result is not None:
    res = st.session_state.mag_calc_result
    st.markdown("### 📊 Calculation Result")

    st.dataframe(st.session_state.mag_calc_table, use_container_width=True)

    st.markdown(
        f"""
        <div class="summary-box">
        <h4>Total container fraction: {res['total_fraction']:.3f}</h4>
        <h3>🛳 Required full containers: <strong>{res['total_containers']}</strong></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Export to Excel
    output = BytesIO()
    st.session_state.mag_calc_table.to_excel(output, index=False)
    output.seek(0)
    st.download_button(
        label="📤 Export Calculation to Excel",
        data=output,
        file_name="Magazine_Container_Calc.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



