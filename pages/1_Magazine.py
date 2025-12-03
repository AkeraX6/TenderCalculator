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

# ---------------------- CSS ----------------------
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

div.block-container {
    padding-top: 5px !important;
    max-width: 1200px;
}

/* Global button style */
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
    padding: 8px 10px;
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

# ---------------------- LOAD PRODUCT LIST ----------------------
@st.cache_data
def load_products():
    df = pd.read_csv("data/Products_TEST.csv")

    # Ensure numeric types
    for col in ["BoxesPerPallet", "PiecesPerBox", "PalletsPerContainer"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

try:
    df_products = load_products()
except Exception:
    st.error("❌ Could not load data/Products_TEST.csv. Check the path and file.")
    st.stop()

required_cols = {"ProductName", "BoxesPerPallet", "PiecesPerBox", "PalletsPerContainer"}
missing = required_cols - set(df_products.columns)
if missing:
    st.error(f"❌ Missing columns in Products_TEST.csv: {missing}")
    st.stop()

# ---------------------- SESSION STATE ----------------------
# Each item: {product, qty, unit}
if "mag_items" not in st.session_state:
    st.session_state.mag_items = []
if "mag_result" not in st.session_state:
    st.session_state.mag_result = None
if "mag_table" not in st.session_state:
    st.session_state.mag_table = None

# ---------------------- TITLE ----------------------
st.markdown(
    "<h2 style='text-align:center;'>📦 Magazine Container Calculator</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;font-style:italic;'>"
    "Add products requested by the client, then click "
    "<strong>Calculate containers</strong>."
    "</p>",
    unsafe_allow_html=True
)
st.write("")

# ---------------------- ADD PRODUCT BAR ----------------------
st.markdown("### ➕ Add product")

add_c1, add_c2, add_c3, add_c4 = st.columns([3, 1.4, 1.2, 1.0])

with add_c1:
    add_product = st.selectbox("Product", df_products["ProductName"], key="add_product")

with add_c2:
    add_qty = st.number_input("Quantity", min_value=1, value=1, key="add_qty")

with add_c3:
    add_unit = st.selectbox("UDM", ["Boxes", "Pcs"], key="add_unit")

with add_c4:
    st.write("")  # push button down to align
    st.write("")
    if st.button("➕ Add", key="btn_add"):
        st.session_state.mag_items.append(
            {"product": add_product, "qty": int(add_qty), "unit": add_unit}
        )
        st.session_state.mag_result = None
        st.session_state.mag_table = None
        st.success(f"{add_product} added.")

st.write("")
st.markdown("### 🧾 Products list")

# ---------------------- PRODUCT ROWS (EDIT / DELETE) ----------------------
if len(st.session_state.mag_items) == 0:
    st.info("No products added yet. Use the 'Add' line above to insert items.")
else:
    for i, item in enumerate(st.session_state.mag_items):
        st.markdown("<div class='product-row'>", unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns([3, 1.2, 1.2, 1, 1])

        with c1:
            st.text(item["product"])

        with c2:
            new_qty = st.number_input(
                "Qty", min_value=1, value=int(item["qty"]), key=f"qty_{i}"
            )

        with c3:
            new_unit = st.selectbox(
                "UDM", ["Boxes", "Pcs"],
                index=0 if item["unit"] == "Boxes" else 1,
                key=f"unit_{i}"
            )

        with c4:
            st.write("")
            if st.button("✏ Update", key=f"update_{i}"):
                item["qty"] = int(new_qty)
                item["unit"] = new_unit
                st.session_state.mag_result = None
                st.session_state.mag_table = None
                st.success(f"Row {i+1} updated.")
                st.rerun()

        with c5:
            st.write("")
            if st.button("🗑 Delete", key=f"delete_{i}"):
                st.session_state.mag_items.pop(i)
                st.session_state.mag_result = None
                st.session_state.mag_table = None
                st.warning(f"Row {i+1} deleted.")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🗑 Clear all products"):
        st.session_state.mag_items = []
        st.session_state.mag_result = None
        st.session_state.mag_table = None
        st.warning("All products cleared.")
        st.rerun()

# ---------------------- CALCULATION LOGIC ----------------------
def calculate_containers(items, df_ref):
    rows = []
    total_fraction = 0.0

    for item in items:
        prod_name = item["product"]
        qty = int(item["qty"])
        unit = item["unit"]

        prod_row = df_ref[df_ref["ProductName"] == prod_name]
        if prod_row.empty:
            continue

        boxes_per_pallet = float(prod_row["BoxesPerPallet"].iloc[0])
        pieces_per_box = float(prod_row["PiecesPerBox"].iloc[0])
        pallets_per_container = float(prod_row["PalletsPerContainer"].iloc[0])

        if pallets_per_container <= 0:
            pallets_per_container = 40  # default if missing

        # 1) Quantity → Boxes
        if unit == "Pcs" and pieces_per_box > 0:
            boxes = math.ceil(qty / pieces_per_box)
        else:
            boxes = qty  # already in boxes

        # 2) Boxes → Pallets
        if boxes_per_pallet > 0:
            pallets = math.ceil(boxes / boxes_per_pallet)
        else:
            pallets = 0

        # 3) Pallets → Container fraction
        fraction = pallets / pallets_per_container if pallets_per_container > 0 else 0.0
        total_fraction += fraction

        rows.append({
            "Product": prod_name,
            "Qty entered": qty,
            "Unit entered": unit,
            "Boxes (calc)": boxes,
            "Pallets": pallets,
            "Container fraction": round(fraction, 3)
        })

    total_containers = math.ceil(total_fraction)

    return rows, total_fraction, total_containers

st.write("")
st.markdown("---")

# ---------------------- CALCULATE BUTTON (CENTERED) ----------------------
if len(st.session_state.mag_items) > 0:
    left, mid, right = st.columns([3, 2, 3])
    with mid:
        calc_clicked = st.button("Calculate containers", key="btn_calc")
    if calc_clicked:
        rows, total_fraction, total_containers = calculate_containers(
            st.session_state.mag_items, df_products
        )
        st.session_state.mag_table = pd.DataFrame(rows)
        st.session_state.mag_result = {
            "fraction": total_fraction,
            "containers": total_containers
        }

# ---------------------- SHOW RESULTS ----------------------
if st.session_state.mag_result is not None:
    res = st.session_state.mag_result
    st.markdown("### 📊 Calculation result")

    st.dataframe(st.session_state.mag_table, use_container_width=True)

    st.markdown(
        f"""
        <div class="summary-box">
          <h4>Total container fraction: {res['fraction']:.3f}</h4>
          <h3>Required full containers: <strong>{res['containers']}</strong></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CSV export (no openpyxl dependency)
    csv_data = st.session_state.mag_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📤 Download CSV",
        data=csv_data,
        file_name="Magazine_Container_Calc.csv",
        mime="text/csv"
    )

