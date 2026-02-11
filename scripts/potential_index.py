"""Potential Index — forward-looking assessment of manager ceiling."""

import math
import pandas as pd


def age_factor(age: float, peak: float = 43.0, sigma: float = 8.0) -> float:
    """
    Gaussian age scoring. Peak potential around age 43 — proven but with runway.

    Examples:
        age 38: 0.90, age 43: 1.00, age 48: 0.90, age 53: 0.63
    """
    return math.exp(-0.5 * ((age - peak) / sigma) ** 2)


def calculate_trend_score(
    current_npxgd: float, prev_npxgd: float,
    current_ppda: float, prev_ppda: float,
    current_league_pct: float, prev_league_pct: float
) -> float:
    """
    Calculate trend from season-over-season KPI improvements.

    Each metric contributes an improvement signal (positive = getting better).
    Combined as weighted average, then mapped to 0-1 via linear scaling.
    """
    npxgd_delta = current_npxgd - prev_npxgd
    ppda_delta = prev_ppda - current_ppda  # inverted: lower ppda is better
    league_delta = current_league_pct - prev_league_pct

    # Normalize each delta to roughly -1 to +1 range
    npxgd_norm = max(-1, min(1, npxgd_delta / 0.15))
    ppda_norm = max(-1, min(1, ppda_delta / 2.0))
    league_norm = max(-1, min(1, league_delta / 20.0))

    # Weighted combination
    raw = 0.4 * npxgd_norm + 0.3 * ppda_norm + 0.3 * league_norm

    # Map to 0-1 (0.5 = stable, >0.5 = improving, <0.5 = declining)
    return max(0.0, min(1.0, 0.5 + raw * 0.5))


def calculate_temperament_score(
    touchline_bans: int,
    public_disagreements: int,
    mid_season_departures: int,
    contract_years_remaining: float,
    config: dict = None
) -> float:
    """
    Derive temperament from observable, documentable facts.

    Base score of 1.0, deductions for incidents, bonus for stability.
    """
    cfg = config or {
        "touchline_ban_penalty": 0.10,
        "public_disagreement_penalty": 0.15,
        "mid_season_departure_penalty": 0.25,
        "contract_years_bonus": 0.05,
    }

    score = 1.0
    score -= touchline_bans * cfg["touchline_ban_penalty"]
    score -= public_disagreements * cfg["public_disagreement_penalty"]
    score -= mid_season_departures * cfg["mid_season_departure_penalty"]
    score += min(contract_years_remaining * cfg["contract_years_bonus"], 0.15)

    return max(0.0, min(1.0, score))


def calculate_resource_leverage(
    league_finish_pct: float,
    squad_value_rank_pct: float,
    scale_factor: float = 2.0
) -> float:
    """
    How much the manager overperforms relative to resources.

    Positive difference = overperforming (finishing higher than squad value suggests).
    Mapped to 0-1 where 0.5 = performing as expected.
    """
    overperformance = league_finish_pct - squad_value_rank_pct
    scaled = overperformance / 100.0 * scale_factor
    return max(0.0, min(1.0, 0.5 + scaled))


def calculate_potential_index(
    df: pd.DataFrame,
    meta_df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Calculate the Potential Index for all managers.

    Components: age_factor, trend_score, resource_leverage, temperament.
    Weighted combination mapped to 0-100 scale.
    """
    df = df.copy()
    pot_cfg = config["potential_index"]
    weights = pot_cfg["weights"]
    age_cfg = pot_cfg["age_curve"]
    temp_cfg = pot_cfg.get("temperament", {})
    leverage_cfg = pot_cfg.get("resource_leverage", {})

    # Merge metadata
    merged = df.merge(meta_df, on="manager_name", how="left", suffixes=("", "_meta"))

    # Age factor
    merged["pot_age"] = merged["age"].apply(
        lambda a: age_factor(a, peak=age_cfg["peak_age"], sigma=age_cfg["sigma"])
    ).round(3)

    # Trend score
    merged["pot_trend"] = merged.apply(
        lambda row: calculate_trend_score(
            current_npxgd=row["npxgd_90"],
            prev_npxgd=row.get("prev_npxgd_90", row["npxgd_90"]),
            current_ppda=row["ppda"],
            prev_ppda=row.get("prev_ppda", row["ppda"]),
            current_league_pct=row.get("league_finish_pct", 50.0),
            prev_league_pct=row.get("prev_league_pos_pct", 50.0),
        ),
        axis=1
    ).round(3)

    # Resource leverage
    merged["pot_leverage"] = merged.apply(
        lambda row: calculate_resource_leverage(
            league_finish_pct=row.get("league_finish_pct", 50.0),
            squad_value_rank_pct=row.get("squad_value_rank_pct", 50.0),
            scale_factor=leverage_cfg.get("scale_factor", 2.0)
        ),
        axis=1
    ).round(3)

    # Temperament
    merged["pot_temperament"] = merged.apply(
        lambda row: calculate_temperament_score(
            touchline_bans=int(row.get("touchline_bans_3yr", 0)),
            public_disagreements=int(row.get("public_disagreements", 0)),
            mid_season_departures=int(row.get("mid_season_departures", 0)),
            contract_years_remaining=float(row.get("contract_years_remaining", 0)),
            config=temp_cfg
        ),
        axis=1
    ).round(3)

    # Weighted combination → 0-100
    merged["potential_index"] = (
        100 * (
            weights["age_factor"] * merged["pot_age"]
            + weights["trend_factor"] * merged["pot_trend"]
            + weights["resource_leverage"] * merged["pot_leverage"]
            + weights["temperament_factor"] * merged["pot_temperament"]
        )
    ).round(1)

    # Copy results back to df
    pot_cols = ["pot_age", "pot_trend", "pot_leverage", "pot_temperament", "potential_index"]
    for col in pot_cols:
        df[col] = merged[col].values

    return df
