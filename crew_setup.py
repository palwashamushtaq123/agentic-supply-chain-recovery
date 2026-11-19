import os
import time
from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool

load_dotenv()

FALLBACK_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
]


def build_llm(model_name: str, api_key: str) -> LLM:
    return LLM(
        model=f"gemini/{model_name}",
        api_key=api_key,
        temperature=0.25,
    )


# ---------------- Custom Python Tools ---------------- #

class StockCoverInput(BaseModel):
    daily_demand: float = Field(..., description="Average units needed per day. Use -1 if unknown.")
    current_stock: float = Field(..., description="Current available units in warehouse. Use -1 if unknown.")
    delay_days: int = Field(..., description="Expected shipment delay in days. Use -1 if unknown.")


class StockCoverTool(BaseTool):
    name: str = "calculate_stock_coverage"
    description: str = (
        "Calculates days of inventory remaining before stockout and flags gaps "
        "when demand, stock, or delay data is missing (-1)."
    )
    args_schema: Type[BaseModel] = StockCoverInput

    def _run(self, daily_demand: float, current_stock: float, delay_days: int) -> str:
        missing = []
        if daily_demand <= 0:
            missing.append("daily_demand")
        if current_stock < 0:
            missing.append("current_stock")
        if delay_days < 0:
            missing.append("delay_days")

        if missing:
            return (
                f"INCOMPLETE_DATA: Missing {', '.join(missing)}. "
                "Apply conservative safety buffer (assume 20% demand surge and +3 days delay) "
                "and list exact data points needed to confirm."
            )

        days_of_cover = round(current_stock / daily_demand, 1)
        shortfall_units = max(0.0, round((delay_days - days_of_cover) * daily_demand, 1))
        status = "CRITICAL_SHORTFALL" if days_of_cover < delay_days else "BUFFER_SUFFICIENT"
        return (
            f"STATUS={status} | Days_of_Cover={days_of_cover}d | "
            f"Delay={delay_days}d | Estimated_Shortfall_Units={shortfall_units}"
        )


class RerouteCostInput(BaseModel):
    units: float = Field(..., description="Number of units to move.")
    mode: str = Field(..., description="Transport mode: 'air', 'express_road', or 'alt_sea_rail'.")
    distance_km: float = Field(..., description="Approx route distance in km.")


class RerouteCostTool(BaseTool):
    name: str = "estimate_reroute_option"
    description: str = "Estimates transit time and rough cost impact for alternative logistics modes."
    args_schema: Type[BaseModel] = RerouteCostInput

    def _run(self, units: float, mode: str, distance_km: float) -> str:
        mode_clean = mode.lower().strip()
        rates = {
            "air": (0.18, 1.5),
            "express_road": (0.06, 3.0),
            "alt_sea_rail": (0.02, 7.0),
        }
        factor, transit_days = rates.get(mode_clean, (0.08, 4.0))
        safe_units = max(100.0, units if units > 0 else 500.0)
        safe_dist = max(50.0, distance_km if distance_km > 0 else 600.0)
        est_cost = round(max(500.0, safe_units * (safe_dist / 100.0) * factor), 2)
        return (
            f"Mode={mode_clean} | Est_Transit_Days={transit_days}d | "
            f"Est_Logistics_Cost_USD=${est_cost}"
        )


def compute_local_baseline_report(crisis_brief: str, priority_mode: str) -> str:
    """Deterministic fallback report using the same Python tools if API quota/503 blocks calls."""
    stock_tool = StockCoverTool()
    reroute_tool = RerouteCostTool()

    triage_info = stock_tool._run(daily_demand=-1, current_stock=1200, delay_days=-1)
    air_opt = reroute_tool._run(units=600, mode="air", distance_km=650)
    road_opt = reroute_tool._run(units=1200, mode="express_road", distance_km=650)

    return (
        f"### 1. Disruption & Risk Triage\n"
        f"- **Scenario Analyzed:** {crisis_brief[:240]}...\n"
        f"- **Tool Result:** {triage_info}\n\n"
        f"### 2. Alternative Sourcing & Logistics ({priority_mode})\n"
        f"- **Fast Bridge (Air):** {air_opt}\n"
        f"- **Primary Reroute (Express Road):** {road_opt}\n\n"
        f"### 3. Recovery Playbook (0–24h & 24–72h)\n"
        f"- **0–24 Hours:** Lock remaining stock for top-priority orders, contact backup depot, and confirm missing demand/delay figures.\n"
        f"- **24–72 Hours:** Dispatch split shipment via Express Road + Air buffer if stock cover is shorter than delay.\n"
        f"- **Contingency Trigger:** If actual delay exceeds 7 days or demand is higher than estimated, cap non-critical allocations immediately."
    )


def _execute_crew(llm: LLM, crisis_brief: str, priority_mode: str) -> str:
    stock_tool = StockCoverTool()
    reroute_tool = RerouteCostTool()

    disruption_analyst = Agent(
        role="Disruption & Risk Analyst",
        goal="Diagnose bottlenecks, quantify stock exposure, and flag missing info without guessing.",
        backstory="Supply chain risk specialist focused on facts, stock math, and blind spots.",
        tools=[stock_tool],
        llm=llm,
        max_iter=2,
        verbose=False,
    )

    logistics_optimizer = Agent(
        role="Alternative Sourcing & Logistics Optimizer",
        goal=f"Compare transport modes and split shipments prioritizing '{priority_mode}'.",
        backstory="Logistics specialist balancing transit speed and cost trade-offs.",
        tools=[reroute_tool],
        llm=llm,
        max_iter=2,
        verbose=False,
    )

    recovery_strategist = Agent(
        role="Executive Recovery Strategist",
        goal="Produce a clear 0-24h, 24-72h playbook with fallback rules for missing data.",
        backstory="Operations leader turning risk and route data into decisive action.",
        llm=llm,
        max_iter=2,
        verbose=False,
    )

    triage_task = Task(
        description=(
            f"Crisis:\n{crisis_brief}\n\n"
            "Call `calculate_stock_coverage` once (-1 for unknown values). "
            "Give concise bullets: Root Cause, Stock Exposure, Missing Data & Safety Buffer."
        ),
        expected_output="Concise risk triage with tool output and missing data list.",
        agent=disruption_analyst,
    )

    routing_task = Task(
        description=(
            f"Priority: {priority_mode}. Call `estimate_reroute_option` for 2 modes. "
            "Compare speed vs cost and state how to adapt if missing numbers are worse."
        ),
        expected_output="Concise route comparison with cost/time and adaptation rule.",
        agent=logistics_optimizer,
        context=[triage_task],
    )

    strategy_task = Task(
        description=(
            f"Priority: {priority_mode}. Write a crisp Recovery Playbook:\n"
            "1) Immediate Actions (0-24h)\n2) Stabilization (24-72h)\n"
            "3) Contingency Triggers for Unknowns\n4) Top Questions to Confirm"
        ),
        expected_output="Actionable 0-24h and 24-72h playbook with triggers.",
        agent=recovery_strategist,
        context=[triage_task, routing_task],
    )

    crew = Crew(
        agents=[disruption_analyst, logistics_optimizer, recovery_strategist],
        tasks=[triage_task, routing_task, strategy_task],
        process=Process.sequential,
        verbose=False,
    )
    return str(crew.kickoff())


def run_crisis_crew(
    crisis_brief: str,
    key_index: int = 1,
    priority_mode: str = "Balanced (Speed + Cost)",
    preferred_model: str = "gemini-3.6-flash",
    allow_offline_fallback: bool = True,
) -> tuple[str, str]:
    key1 = os.getenv("GOOGLE_API_KEY_1", "").strip()
    key2 = os.getenv("GOOGLE_API_KEY_2", "").strip()

    keys_to_try = []
    if key_index == 1:
        if key1:
            keys_to_try.append(("GOOGLE_API_KEY_1", key1))
        if key2:
            keys_to_try.append(("GOOGLE_API_KEY_2", key2))
    else:
        if key2:
            keys_to_try.append(("GOOGLE_API_KEY_2", key2))
        if key1:
            keys_to_try.append(("GOOGLE_API_KEY_1", key1))

    models_to_try = [preferred_model] + [m for m in FALLBACK_MODELS if m != preferred_model]
    last_error = None

    if keys_to_try:
        for model_name in models_to_try:
            for key_label, api_key in keys_to_try:
                try:
                    llm = build_llm(model_name, api_key)
                    output = _execute_crew(llm, crisis_brief, priority_mode)
                    return output, f"{model_name} via {key_label}"
                except Exception as exc:
                    last_error = exc
                    err_str = str(exc)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        time.sleep(8)
                    elif "503" in err_str or "UNAVAILABLE" in err_str:
                        time.sleep(2)
                    continue

    if allow_offline_fallback:
        baseline = compute_local_baseline_report(crisis_brief, priority_mode)
        return baseline, f"Resilient Tool Baseline (API busy/quota hit: {str(last_error)[:90]})"

    raise RuntimeError(f"All attempts failed. Last error: {last_error}")