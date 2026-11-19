import streamlit as st
from crew_setup import run_crisis_crew, FALLBACK_MODELS
from sample_crises import SCENARIOS

st.set_page_config(
    page_title="Supply Chain Crisis Command",
    page_icon="⚡",
    layout="wide",
)

# ---------------- Custom HTML & CSS ---------------- #
st.markdown(
    """
    <style>
        .main-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #0f766e 100%);
            padding: 24px 28px;
            border-radius: 16px;
            color: #f8fafc;
            border: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 18px;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
        }
        .main-header h1 {
            margin: 0 0 6px 0;
            font-size: 1.9rem;
            font-weight: 700;
            color: #ffffff;
        }
        .main-header p {
            margin: 0;
            color: #cbd5e1;
            font-size: 0.96rem;
        }
        .badge-row {
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .pill {
            background: rgba(255,255,255,0.12);
            color: #e2e8f0;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.15);
        }
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin: 14px 0 20px 0;
        }
        @media (max-width: 900px) {
            .agent-grid {
                grid-template-columns: 1fr;
            }
        }
        .agent-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-top: 4px solid #0f766e;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        }
        .agent-card.blue { border-top-color: #2563eb; }
        .agent-card.amber { border-top-color: #d97706; }
        .agent-title {
            font-weight: 700;
            font-size: 1rem;
            color: #0f172a;
            margin-bottom: 6px;
        }
        .agent-desc {
            font-size: 0.86rem;
            color: #475569;
            line-height: 1.45;
            margin-bottom: 8px;
        }
        .tool-tag {
            display: inline-block;
            background: #f1f5f9;
            color: #0f172a;
            font-family: monospace;
            font-size: 0.76rem;
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
        }
        .flow-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 14px;
            padding: 16px;
            margin-top: 10px;
        }
        .flow-step {
            background: #ffffff;
            border-left: 4px solid #0f766e;
            padding: 8px 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            font-size: 0.84rem;
            color: #1e293b;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Header ---------------- #
st.markdown(
    """
    <div class="main-header">
        <h1>⚡ Supply Chain Crisis Command</h1>
        <p>Multi-Agent Disruption Triage, Logistics Optimization & Recovery Playbook Engine</p>
        <div class="badge-row">
            <span class="pill">CrewAI Sequential Pipeline</span>
            <span class="pill">Gemini 3.6 Flash + Auto Fallback</span>
            <span class="pill">Dual API Key Resilience</span>
            <span class="pill">Missing-Data Safety Guardrails</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- 3 Agent Overview Cards ---------------- #
st.markdown(
    """
    <div class="agent-grid">
        <div class="agent-card">
            <div class="agent-title">1. Disruption & Risk Analyst</div>
            <div class="agent-desc">Calculates stock runway, flags missing numbers (-1), and applies safety buffers instead of guessing.</div>
            <span class="tool-tag">Tool: calculate_stock_coverage</span>
        </div>
        <div class="agent-card blue">
            <div class="agent-title">2. Logistics Optimizer</div>
            <div class="agent-desc">Compares air, express road, and sea/rail transit days & costs based on your chosen priority mode.</div>
            <span class="tool-tag">Tool: estimate_reroute_option</span>
        </div>
        <div class="agent-card amber">
            <div class="agent-title">3. Recovery Strategist</div>
            <div class="agent-desc">Builds 0–24h and 24–72h action plans, contingency triggers, and supplier verification questions.</div>
            <span class="tool-tag">Output: Executive Playbook</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Sidebar Controls & Flowchart ---------------- #
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

    st.divider()
    st.markdown("### 🔀 System Flowchart")
    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-step"><b>1. Crisis Input</b><br/>Scenario + Optional Metrics</div>
            <div class="flow-step"><b>2. Risk Analyst</b><br/>Stock math + Missing-data check</div>
            <div class="flow-step"><b>3. Logistics Optimizer</b><br/>Air / Road / Rail trade-offs</div>
            <div class="flow-step"><b>4. Recovery Strategist</b><br/>0–24h & 72h Playbook + Fallback</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Scenario & Optional Structured Inputs ---------------- #
col_left, col_right = st.columns([1.45, 1])

with col_left:
    preset = st.selectbox("Load Sample Scenario", ["Custom"] + list(SCENARIOS.keys()))
    default_text = "" if preset == "Custom" else SCENARIOS[preset]

    crisis_text = st.text_area(
        "Crisis Description",
        value=default_text,
        height=135,
        placeholder="Describe supplier failure, delay, stock status, or unknown figures...",
    )

with col_right:
    st.markdown("**Optional Structured Override (Leave -1 if unknown)**")
    c1, c2 = st.columns(2)
    with c1:
        stock_val = st.number_input("Current Stock (units)", min_value=-1, value=-1, step=100)
        delay_val = st.number_input("Delay Days", min_value=-1, value=-1, step=1)
    with c2:
        demand_val = st.number_input("Daily Demand (units/day)", min_value=-1, value=-1, step=50)
        dist_val = st.number_input("Backup Route (km)", min_value=-1, value=-1, step=50)

# Merge optional overrides cleanly if user changed any from -1
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

# ---------------- Run Analysis ---------------- #
if st.button("🚀 Launch Multi-Agent Crisis Analysis", type="primary", use_container_width=True):
    if not final_crisis_brief:
        st.warning("Please enter a crisis scenario or select a sample scenario first.")
    else:
        with st.spinner("Agents collaborating on risk triage, rerouting, and recovery strategy..."):
            try:
                output, used_label = run_crisis_crew(
                    crisis_brief=final_crisis_brief,
                    key_index=key_choice,
                    priority_mode=priority_mode,
                    preferred_model=preferred_model,
                )
                st.success(f"Completed using: **{used_label}** | Priority: **{priority_mode}**")
                st.markdown(output)

                st.download_button(
                    "📥 Download Recovery Playbook (.md)",
                    data=output,
                    file_name="supply_chain_recovery_playbook.md",
                    mime="text/markdown",
                )
            except Exception as e:
                st.error(f"Execution failed: {e}")