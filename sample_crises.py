SCENARIOS = {
    "Port Strike + Tier-1 Supplier Halt (Complete Data)": (
        "Primary electronics component supplier in East Asia halted production due to a factory power/equipment "
        "issue. Current warehouse stock is 4,500 units, average daily demand is 600 units/day, and the next "
        "scheduled sea shipment is delayed by 14 days. Route distance from secondary regional hub is ~1,400 km."
    ),
    "Incomplete Info: Missing Demand & Delay (Edge Case)": (
        "A key packaging supplier missed delivery and a regional highway is partially blocked. "
        "Warehouse has roughly 1,200 units left, daily demand isn't updated in the system yet, "
        "and the carrier hasn't confirmed total delay days. Distance to backup depot is ~650 km."
    ),
    "Pharma Cold-Chain + Customs Hold (High Urgency)": (
        "Temperature-sensitive medical kits are held at port customs for an estimated 6 days while primary "
        "cold-storage vendor faces power outages. Current stock is 2,100 units, daily hospital demand is "
        "450 units/day, and alternate regional hub is 900 km away."
    ),
}