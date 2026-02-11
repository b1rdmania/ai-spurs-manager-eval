"""Data loading and validation for manager evaluation pipeline."""

import pandas as pd
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_config(config_path: str = None) -> dict:
    """Load the unified scoring configuration."""
    path = Path(config_path) if config_path else BASE_DIR / "config" / "scoring.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def load_managers(csv_path: str = None) -> pd.DataFrame:
    """Load and validate the managers KPI dataset."""
    path = Path(csv_path) if csv_path else BASE_DIR / "data" / "managers.csv"
    df = pd.read_csv(path)
    errors = validate_managers(df)
    if errors:
        raise ValueError(f"Manager data validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    return df


def load_meta(csv_path: str = None) -> pd.DataFrame:
    """Load and validate the managers metadata."""
    path = Path(csv_path) if csv_path else BASE_DIR / "data" / "managers_meta.csv"
    df = pd.read_csv(path)
    errors = validate_meta(df)
    if errors:
        raise ValueError(f"Manager metadata validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    return df


REQUIRED_KPI_COLUMNS = [
    "manager_name", "ppda", "oppda", "high_press_regains_90",
    "npxgd_90", "xg_per_shot", "xg_open_play_90", "xga_90",
    "big6_w", "big6_l", "big6_d", "ko_win_rate",
    "u23_minutes_pct", "academy_debuts", "youth_progression_count",
    "injury_days_season", "player_availability", "squad_rotation_index",
    "squad_value_delta_m", "net_spend_m", "sell_on_profit_m",
    "fan_sentiment_pct", "media_vol_sigma"
]

REQUIRED_META_COLUMNS = [
    "manager_name", "slug", "age", "nationality", "current_club",
    "available", "touchline_bans_3yr", "public_disagreements",
    "mid_season_departures", "contract_years_remaining",
    "board_backing_score",
    "prev_npxgd_90", "prev_ppda", "prev_league_pos_pct",
    "squad_value_rank_pct", "league_finish_pct"
]

# Sensible ranges for validation (min, max)
KPI_RANGES = {
    "ppda": (4, 20),
    "oppda": (4, 20),
    "high_press_regains_90": (1, 15),
    "npxgd_90": (-1.0, 1.0),
    "xg_per_shot": (0.03, 0.20),
    "xg_open_play_90": (0.2, 3.0),
    "xga_90": (0.3, 2.5),
    "big6_w": (0, 20),
    "big6_l": (0, 20),
    "big6_d": (0, 15),
    "ko_win_rate": (0, 100),
    "u23_minutes_pct": (0, 50),
    "academy_debuts": (0, 20),
    "youth_progression_count": (0, 15),
    "injury_days_season": (100, 2000),
    "player_availability": (50, 100),
    "squad_rotation_index": (0.1, 0.9),
    "squad_value_delta_m": (-200, 500),
    "net_spend_m": (-200, 400),
    "sell_on_profit_m": (0, 300),
    "fan_sentiment_pct": (5, 95),
    "media_vol_sigma": (0.3, 3.0),
}


def validate_managers(df: pd.DataFrame) -> list[str]:
    """Validate the managers KPI dataframe. Returns list of error strings."""
    errors = []

    # Check required columns
    missing = set(REQUIRED_KPI_COLUMNS) - set(df.columns)
    if missing:
        errors.append(f"Missing columns: {sorted(missing)}")
        return errors  # Can't validate further without columns

    # Check no duplicate managers
    dupes = df["manager_name"].duplicated()
    if dupes.any():
        errors.append(f"Duplicate managers: {df.loc[dupes, 'manager_name'].tolist()}")

    # Check no null values in required columns
    for col in REQUIRED_KPI_COLUMNS:
        nulls = df[col].isna().sum()
        if nulls > 0:
            errors.append(f"Column '{col}' has {nulls} null value(s)")

    # Check numeric ranges
    for col, (lo, hi) in KPI_RANGES.items():
        if col in df.columns:
            out_of_range = df[(df[col] < lo) | (df[col] > hi)]
            for _, row in out_of_range.iterrows():
                errors.append(
                    f"{row['manager_name']}: {col}={row[col]} outside range [{lo}, {hi}]"
                )

    return errors


def validate_meta(df: pd.DataFrame) -> list[str]:
    """Validate the managers metadata dataframe."""
    errors = []

    missing = set(REQUIRED_META_COLUMNS) - set(df.columns)
    if missing:
        errors.append(f"Missing columns: {sorted(missing)}")
        return errors

    # Check ages are reasonable for football managers
    for _, row in df.iterrows():
        if not (30 <= row["age"] <= 70):
            errors.append(f"{row['manager_name']}: age={row['age']} outside range [30, 70]")

    return errors


def compute_derived_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived KPI columns computed from base data."""
    df = df.copy()

    # Big 6 win percentage
    big6_total = df["big6_w"] + df["big6_l"] + df["big6_d"]
    df["big6_win_pct"] = (df["big6_w"] / big6_total.replace(0, 1) * 100).round(1)

    # Big 6 xG difference proxy: (wins - losses) / total games as a simple approximation
    # This is a rough proxy when we don't have actual xG data per big6 game
    df["big6_xgd"] = ((df["big6_w"] - df["big6_l"]) / big6_total.replace(0, 1)).round(3)

    return df
