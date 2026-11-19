import pandas as pd
import streamlit as st
from crew_setup import run_crisis_crew, FALLBACK_MODELS
from sample_crises import SCENARIOS
from styles import (
    apply_styles,
    render_header,
    render_agent_cards,
    render_sidebar_highlight,
    render_sidebar_flowchart,
)
from pdf_export import markdown_to_pdf_bytes

st.set_page_config(
    page_title="Supply Chain Crisis Command",
    page_icon="⚡",
    layout="wide",
)

# ---------------- Styles, Header & Agent Cards ---------------- #
apply_styles()
render_header()
render_agent_cards()

# ---------------- Sidebar Controls & Highlighted Flowchart ---------------- #
with st.sidebar:
    st.header("🎛️ Control Panel")
    key_choice = st.radio(
        "Primary Gemini API Key",
        options=[1, 2],
        format_func=lambda x: f"GOOGLE_API_KEY_{x}",
        index=0,
    )
    preferred_model = st.selectbox(
        "Primary Model (Auto-falls back on 503)",
        options=FALLBACK_MODELS,
        index=0,
    )
    priority_mode = st.selectbox(
        "Decision Priority Mode",
        options=[
            "Balanced (Speed + Cost)",
            "Fastest Recovery (Minimize Stockout)",
            "Lowest Cost (Budget Protection)",
        ],
    )

    render_sidebar_highlight(priority_mode, preferred_model)

    st.divider()
    st.markdown("### 🔀 System Flowchart")
    render_sidebar_flowchart()

# ---------------- Scenario & Optional Structured Inputs ---------------- #
col_left, col_right = st.columns([1.45, 1])

with col_left:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    preset = st.selectbox("Load Sample Scenario", ["Custom"] + list(SCENARIOS.keys()))
    default_text = "" if preset == "Custom" else SCENARIOS[preset]

    crisis_text = st.text_area(
        "Crisis Description",
        value=default_text,
        height=135,
        placeholder="Describe supplier failure, delay, stock status, or unknown figures...",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("**Optional Structured Override (Leave -1 if unknown)**")
    c1, c2 = st.columns(2)
    with c1:
        stock_val = st.number_input("Current Stock (units)", min_value=-1, value=-1, step=100)
        delay_val = st.number_input("Delay Days", min_value=-1, value=-1, step=1)
    with c2:
        demand_val = st.number_input("Daily Demand (units/day)", min_value=-1, value=-1, step=50)
        dist_val = st.number_input("Backup Route (km)", min_value=-1, value=-1, step=50)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Optional CSV / ERP Data Upload ---------------- #
st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.markdown("### 📂 Optional: Upload Inventory / ERP CSV")

sample_csv_content = (
    "sku,item_name,current_stock,daily_demand,delay_days,backup_distance_km,notes\n"
    "PKG-101,Corrugated Cartons,1200,-1,-1,650,Primary packaging supplier delayed and highway partially blocked\n"
    "LAB-204,Barcode Labels,450,150,2,180,Secondary vendor available with express road option\n"
    "RAW-309,Polymer Resin,800,320,5,920,Port congestion reported; air or alt rail needed\n"
)

st.download_button(
    label="📥 Download Sample CSV to Test",
    data=sample_csv_content,
    file_name="sample_inventory.csv",
    mime="text/csv",
)

uploaded_csv = st.file_uploader(
    "Upload a CSV file to test with live table data (optional)",
    type=["csv"],
)

csv_context_text = ""
if uploaded_csv is not None:
    try:
        df_csv = pd.read_csv(uploaded_csv)
        st.dataframe(df_csv.head(15), use_container_width=True)

        preview_records = df_csv.head(20).to_dict(orient="records")
        csv_context_text = (
            f"\n\nUploaded CSV Data ({uploaded_csv.name}, {len(df_csv)} total rows):\n"
            f"{preview_records}"
        )
        st.success(f"Loaded {len(df_csv)} rows from `{uploaded_csv.name}`.")
    except Exception as e:
        st.error(f"Could not read CSV file: {e}")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Merge Inputs & Run Analysis ---------------- #
extra_parts = []
if stock_val != -1:
    extra_parts.append(f"Current stock override: {stock_val} units.")
if demand_val != -1:
    extra_parts.append(f"Daily demand override: {demand_val} units/day.")
if delay_val != -1:
    extra_parts.append(f"Expected delay override: {delay_val} days.")
if dist_val != -1:
    extra_parts.append(f"Backup route distance override: {dist_val} km.")

final_crisis_brief = crisis_text.strip()
if extra_parts:
    final_crisis_brief += "\n\nStructured Metrics Provided:\n" + " ".join(extra_parts)
if csv_context_text:
    final_crisis_brief += csv_context_text

if "playbook_result" not in st.session_state:
    st.session_state.playbook_result = None

if st.button("🚀 Launch Multi-Agent Crisis Analysis", type="primary", use_container_width=True):
    if not final_crisis_brief:
        st.warning("Please enter a crisis scenario, upload a CSV, or select a sample scenario first.")
    else:
        with st.spinner("Agents collaborating on risk triage, rerouting, and recovery strategy..."):
            try:
                output, used_label = run_crisis_crew(
                    crisis_brief=final_crisis_brief,
                    key_index=key_choice,
                    priority_mode=priority_mode,
                    preferred_model=preferred_model,
                )
                st.session_state.playbook_result = {
                    "output": output,
                    "used_label": used_label,
                    "priority_mode": priority_mode,
                }
            except Exception as e:
                st.error(f"Execution failed: {e}")

if st.session_state.playbook_result is not None:
    res = st.session_state.playbook_result
    st.success(f"Completed using: **{res['used_label']}** | Priority: **{res['priority_mode']}**")
    st.markdown(res["output"])

    pdf_bytes = markdown_to_pdf_bytes(
        res["output"],
        title="Supply Chain Recovery Playbook",
    )

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📄 Download Recovery Playbook (.pdf)",
            data=pdf_bytes,
            file_name="supply_chain_recovery_playbook.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with col_dl2:
        st.download_button(
            "📥 Download Recovery Playbook (.md)",
            data=res["output"],
            file_name="supply_chain_recovery_playbook.md",
            mime="text/markdown",
            use_container_width=True,
        )