import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f8fafc 0%, #eef2f6 100%);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0b1324 0%, #0f172a 60%, #112a36 100%);
                border-right: 1px solid rgba(45, 212, 191, 0.22);
            }
            [data-testid="stSidebar"] * {
                color: #f1f5f9;
            }
            [data-testid="stSidebar"] .stRadio > div,
            [data-testid="stSidebar"] .stSelectbox > div > div {
                background: rgba(255, 255, 255, 0.06) !important;
                border: 1px solid rgba(148, 163, 184, 0.25) !important;
                border-radius: 10px !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: rgba(148, 163, 184, 0.22);
            }

            .sidebar-highlight-banner {
                background: linear-gradient(135deg, rgba(15, 118, 110, 0.35), rgba(37, 99, 235, 0.25));
                border: 1px solid rgba(45, 212, 191, 0.45);
                border-left: 4px solid #2dd4bf;
                border-radius: 12px;
                padding: 12px 14px;
                margin-bottom: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
            }
            .sidebar-highlight-title {
                font-size: 0.76rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #5eead4;
                font-weight: 700;
                margin-bottom: 4px;
            }
            .sidebar-highlight-sub {
                font-size: 0.82rem;
                color: #e2e8f0;
                line-height: 1.35;
            }

            .main-header {
                background: linear-gradient(135deg, #090d16 0%, #0f172a 52%, #0f766e 100%);
                padding: 26px 30px;
                border-radius: 18px;
                color: #f8fafc;
                border: 1px solid rgba(255,255,255,0.14);
                margin-bottom: 18px;
                box-shadow: 0 14px 30px rgba(15, 23, 42, 0.16);
            }
            .main-header h1 {
                margin: 0 0 6px 0;
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: -0.02em;
                color: #ffffff;
            }
            .main-header p {
                margin: 0;
                color: #cbd5e1;
                font-size: 0.98rem;
            }
            .badge-row {
                margin-top: 14px;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            .pill {
                background: rgba(255,255,255,0.12);
                color: #f8fafc;
                padding: 5px 12px;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                border: 1px solid rgba(255,255,255,0.18);
            }

            .agent-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                margin: 14px 0 22px 0;
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
                border-radius: 16px;
                padding: 18px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
                transition: transform 0.15s ease, box-shadow 0.15s ease;
            }
            .agent-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.1);
            }
            .agent-card.blue { border-top-color: #2563eb; }
            .agent-card.amber { border-top-color: #d97706; }
            .agent-title {
                font-weight: 700;
                font-size: 1.02rem;
                color: #0f172a;
                margin-bottom: 6px;
            }
            .agent-desc {
                font-size: 0.87rem;
                color: #475569;
                line-height: 1.5;
                margin-bottom: 10px;
            }
            .tool-tag {
                display: inline-block;
                background: #f1f5f9;
                color: #0f172a;
                font-family: monospace;
                font-size: 0.76rem;
                font-weight: 600;
                padding: 4px 9px;
                border-radius: 7px;
                border: 1px solid #cbd5e1;
            }

            .flow-box {
                background: rgba(15, 23, 42, 0.65);
                border: 1px solid rgba(45, 212, 191, 0.28);
                border-radius: 14px;
                padding: 12px;
                margin-top: 8px;
            }
            .flow-step {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-left: 4px solid #2dd4bf;
                padding: 9px 12px;
                margin-bottom: 8px;
                border-radius: 10px;
                font-size: 0.83rem;
                color: #f8fafc;
            }
            .flow-step.step-blue { border-left-color: #60a5fa; }
            .flow-step.step-amber { border-left-color: #fbbf24; }
            .flow-step.step-emerald { border-left-color: #34d399; margin-bottom: 0; }
            .flow-step span {
                color: #cbd5e1;
                font-size: 0.78rem;
            }

            .panel-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 18px 20px;
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
                margin-bottom: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
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


def render_agent_cards() -> None:
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


def render_sidebar_highlight(priority_mode: str, model_name: str) -> None:
    st.markdown(
        f"""
        <div class="sidebar-highlight-banner">
            <div class="sidebar-highlight-title">⚡ Active Command Profile</div>
            <div class="sidebar-highlight-sub">
                <b>Mode:</b> {priority_mode}<br/>
                <b>Model:</b> <code>{model_name}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_flowchart() -> None:
    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-step"><b>1. Crisis Input</b><br/><span>Scenario + CSV / Metrics</span></div>
            <div class="flow-step step-blue"><b>2. Risk Analyst</b><br/><span>Stock math + Missing-data check</span></div>
            <div class="flow-step step-amber"><b>3. Logistics Optimizer</b><br/><span>Air / Road / Rail trade-offs</span></div>
            <div class="flow-step step-emerald"><b>4. Recovery Strategist</b><br/><span>0–24h & 72h Playbook + PDF/MD</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )