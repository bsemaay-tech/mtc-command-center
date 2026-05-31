BASE_ROUND_TRIP_COST_PCT = 0.12


def apply_round_trip_cost(gross_return_pct: float, cost_mult: float = 1.0) -> float:
    return gross_return_pct - BASE_ROUND_TRIP_COST_PCT * cost_mult
