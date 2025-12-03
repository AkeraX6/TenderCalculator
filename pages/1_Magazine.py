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

    # HazardCode as string
    if "HazardCode" in df.columns:
        df["HazardCode"] = df["HazardCode"].astype(str)
    else:
        df["HazardCode"] = ""

    return df

try:
    df_products = load_products()
except Exception:
    st.error("❌ Could not load data/Products_TEST.csv. Check the path and file.")
    st.stop()

required_cols = {
    "ProductName",
    "BoxesPerPallet",
    "PiecesPerBox",
    "PalletsPerContainer",
    "HazardCode",
}
missing = required_cols - set(df_products.columns)
if missing:
    st.error(f"❌ Missing columns in Products_TEST.csv: {missing}")
    st.stop()

# ---------------------- SESSION STATE ----------------------
# Each item: {product, qty, unit}
if "mag_items" not in st.session_state:
    st.session_state.mag_items = []
if "mag_calc" not in st.session_state:
    st.session_state.mag_calc = None

# ---------------------- TITLE ----------------------
st.markdown(
    "<h2 style='text-align:center;'>📦 Magazine Container Calculator</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-style:italic;'>"
    "Add products requested by the client, then click "
    "<strong>Calculate containers</strong>."
    "</p>",
    unsafe_allow_html=True,
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
    st.write("")
    st.write("")
    if st.button("➕ Add", key="btn_add"):
        st.session_state.mag_items.append(
            {"product": add_product, "qty": int(add_qty), "unit": add_unit}
        )
        st.session_state.mag_calc = None
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
                "UDM",
                ["Boxes", "Pcs"],
                index=0 if item["unit"] == "Boxes" else 1,
                key=f"unit_{i}",
            )

        with c4:
            st.write("")
            if st.button("✏ Update", key=f"update_{i}"):
                item["qty"] = int(new_qty)
                item["unit"] = new_unit
                st.session_state.mag_calc = None
                st.success(f"Row {i+1} updated.")
                st.rerun()

        with c5:
            st.write("")
            if st.button("🗑 Delete", key=f"delete_{i}"):
                st.session_state.mag_items.pop(i)
                st.session_state.mag_calc = None
                st.warning(f"Row {i+1} deleted.")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🗑 Clear all products"):
        st.session_state.mag_items = []
        st.session_state.mag_calc = None
        st.warning("All products cleared.")
        st.rerun()


# ---------------------- CALCULATION LOGIC ----------------------
def compute_calculation(items, df_ref):
    rows = []
    total_fraction_global = 0.0

    hazard_pallets = {}      # hazard -> total pallets
    hazard_ppc = {}          # hazard -> pallets per container (max of products)
    hazard_products = {}     # hazard -> list of product names

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
        hazard = str(prod_row["HazardCode"].iloc[0]).strip()

        if pallets_per_container <= 0:
            pallets_per_container = 40.0  # fallback default

        # 1) Qty -> Boxes
        if unit == "Pcs" and pieces_per_box > 0:
            boxes = math.ceil(qty / pieces_per_box)
        else:
            boxes = qty  # already in boxes

        # 2) Boxes -> Pallets
        if boxes_per_pallet > 0:
            pallets = math.ceil(boxes / boxes_per_pallet)
        else:
            pallets = 0

        # 3) Pallets -> Container fraction (global, ignoring compatibility)
        fraction = pallets / pallets_per_container if pallets_per_container > 0 else 0.0
        total_fraction_global += fraction

        # Aggregate per hazard
        if hazard not in hazard_pallets:
            hazard_pallets[hazard] = 0.0
        hazard_pallets[hazard] += pallets

        if hazard not in hazard_ppc:
            hazard_ppc[hazard] = pallets_per_container
        else:
            hazard_ppc[hazard] = max(hazard_ppc[hazard], pallets_per_container)

        hazard_products.setdefault(hazard, [])
        if prod_name not in hazard_products[hazard]:
            hazard_products[hazard].append(prod_name)

        rows.append(
            {
                "Product": prod_name,
                "Hazard": hazard,
                "Qty entered": qty,
                "Unit entered": unit,
                "Boxes (calc)": boxes,
                "Pallets": pallets,
                "Container fraction (global)": round(fraction, 3),
            }
        )

    total_containers_global = math.ceil(total_fraction_global)

    # ---- Hazard-based stats (per group) ----
    # Non-friendly hazards (anything except 1.4S)
    non_friendly = [hz for hz in hazard_pallets.keys() if hz != "1.4S"]
    compat_issue = len(non_friendly) > 1

    # PLAN A: only 40 ft (using pallets-per-container from CSV per hazard)
    hazard_stats_planA = []
    total_containers_planA = 0

    for hz, pallets in hazard_pallets.items():
        ppc = hazard_ppc.get(hz, 40.0)
        if hz == "1.4S":
            # 1.4S can go anywhere; we don't assign standalone containers here
            note = "Can be loaded with any other hazard group (1.4S)."
            hazard_stats_planA.append(
                {
                    "Hazard": hz,
                    "Pallets": pallets,
                    "40ft containers": 0,
                    "20ft containers": 0,
                    "Note": note,
                }
            )
            continue

        containers_40 = math.ceil(pallets / ppc)
        total_containers_planA += containers_40

        hazard_stats_planA.append(
            {
                "Hazard": hz,
                "Pallets": pallets,
                "40ft containers": containers_40,
                "20ft containers": 0,
                "Note": "",
            }
        )

    # PLAN B: suggestion using 20 ft for small volumes
    hazard_stats_planB = []
    total_containers_planB_40 = 0
    total_containers_planB_20 = 0

    for hz, pallets in hazard_pallets.items():
        ppc = hazard_ppc.get(hz, 40.0)
        if hz == "1.4S":
            note = "Can be loaded with any other hazard group (1.4S)."
            hazard_stats_planB.append(
                {
                    "Hazard": hz,
                    "Pallets": pallets,
                    "40ft containers": 0,
                    "20ft containers": 0,
                    "Note": note,
                }
            )
            continue

        # assume 40ft holds 'ppc' pallets, 20ft half:
        p40 = ppc
        p20 = max(ppc / 2, 1)

        full_40 = int(pallets // p40)
        rem = pallets % p40

        if rem == 0:
            containers_40 = full_40
            containers_20 = 0
        elif rem <= p20:
            containers_40 = full_40
            containers_20 = 1
        else:
            containers_40 = full_40 + 1
            containers_20 = 0

        total_containers_planB_40 += containers_40
        total_containers_planB_20 += containers_20

        note = ""
        if containers_20 > 0:
            note = "20ft used for small remaining volume."

        hazard_stats_planB.append(
            {
                "Hazard": hz,
                "Pallets": pallets,
                "40ft containers": containers_40,
                "20ft containers": containers_20,
                "Note": note,
            }
        )

    detail_df = pd.DataFrame(rows)
    planA_df = pd.DataFrame(hazard_stats_planA)
    planB_df = pd.DataFrame(hazard_stats_planB)

    return {
        "detail_df": detail_df,
        "total_fraction_global": total_fraction_global,
        "total_containers_global": total_containers_global,
        "compat_issue": compat_issue,
        "hazard_pallets": hazard_pallets,
        "hazard_products": hazard_products,
        "planA_df": planA_df,
        "total_planA": total_containers_planA,
        "planB_df": planB_df,
        "total_planB_40": total_containers_planB_40,
        "total_planB_20": total_containers_planB_20,
    }


st.write("")
st.markdown("---")

# ---------------------- CALCULATE BUTTON (CENTERED) ----------------------
if len(st.session_state.mag_items) > 0:
    left, mid, right = st.columns([3, 2, 3])
    with mid:
        calc_clicked = st.button("🛳 Calculate containers", key="btn_calc")
    if calc_clicked:
        st.session_state.mag_calc = compute_calculation(
            st.session_state.mag_items, df_products
        )

# ---------------------- SHOW RESULTS ----------------------
calc = st.session_state.mag_calc
if calc is not None and not calc["detail_df"].empty:
    st.markdown("### 📊 Detailed calculation per product")
    st.dataframe(calc["detail_df"], use_container_width=True)

    st.markdown(
        f"""
        <div class="summary-box">
          <h4>Total global container fraction (ignoring compatibility): {calc['total_fraction_global']:.3f}</h4>
          <h3>Approx. full containers (global): <strong>{calc['total_containers_global']}</strong></h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------- COMPATIBILITY SECTION ----------------------
    st.markdown("### 🔥 Compatibility & Hazard Split")

    # Non-1.4S hazards present
    non_friendly = [
        hz for hz in calc["hazard_pallets"].keys() if hz != "1.4S"
    ]

    if calc["compat_issue"]:
        st.error(
            "🚨 Explosive Compatibility Alert\n\n"
            f"More than one non-1.4S hazard present: {', '.join(non_friendly)}.\n"
            "These hazard groups must NOT be shipped in the same container."
        )
    else:
        st.success(
            "✅ No critical compatibility issue detected between hazard groups "
            "(ignoring 1.4S, which is broadly compatible)."
        )

    # Show which products belong to each hazard group
    st.markdown("**Hazard groups and products:**")
    for hz, prods in calc["hazard_products"].items():
        st.markdown(f"- **{hz}**: " + ", ".join(prods))

    st.write("")
    plan_choice = st.radio(
        "Container strategy",
        [
            "Plan A — Only 40 ft containers",
            "Plan B — Suggest 20 ft for small volumes",
        ],
        index=0,
    )

    if plan_choice.startswith("Plan A"):
        st.markdown("#### Plan A — Only 40 ft containers")
        st.dataframe(calc["planA_df"], use_container_width=True)
        st.markdown(
            f"**Total 40 ft containers (Plan A):** {calc['total_planA']}"
        )
    else:
        st.markdown("#### Plan B — 40 ft + 20 ft suggestion")
        st.dataframe(calc["planB_df"], use_container_width=True)
        st.markdown(
            f"**Total containers (Plan B):** "
            f"{calc['total_planB_40']} × 40 ft, "
            f"{calc['total_planB_20']} × 20 ft"
        )

    # ---------------------- DOWNLOAD DETAIL CSV ----------------------
    csv_data = calc["detail_df"].to_csv(index=False).encode("utf-8")
    st.download_button(
        "📤 Download detailed calculation (CSV)",
        data=csv_data,
        file_name="Magazine_Container_Calc_Detail.csv",
        mime="text/csv",
    )


