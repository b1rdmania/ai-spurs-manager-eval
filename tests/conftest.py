"""Shared fixtures for scoring engine tests."""

import pytest
import pandas as pd


@pytest.fixture
def sample_managers_df():
    """DataFrame with 3 synthetic managers spanning low/mid/high ranges."""
    return pd.DataFrame({
        "manager_name": ["Low Performer", "Mid Performer", "High Performer"],
        "ppda": [14.0, 10.5, 8.0],
        "oppda": [10.0, 13.0, 16.0],
        "high_press_regains_90": [4.5, 7.0, 9.0],
        "npxgd_90": [0.02, 0.12, 0.28],
        "xg_per_shot": [0.08, 0.10, 0.13],
        "xg_open_play_90": [0.9, 1.3, 1.7],
        "xga_90": [1.5, 1.1, 0.8],
        "big6_w": [1, 3, 6],
        "big6_l": [6, 3, 2],
        "big6_d": [3, 4, 2],
        "ko_win_rate": [25.0, 45.0, 62.0],
        "u23_minutes_pct": [5.0, 12.0, 20.0],
        "academy_debuts": [1, 4, 8],
        "youth_progression_count": [0, 2, 5],
        "injury_days_season": [900, 650, 450],
        "player_availability": [82.0, 89.0, 93.0],
        "squad_rotation_index": [0.55, 0.40, 0.30],
        "squad_value_delta_m": [10.0, 80.0, 180.0],
        "net_spend_m": [150.0, 40.0, -20.0],
        "sell_on_profit_m": [5.0, 25.0, 80.0],
        "fan_sentiment_pct": [25.0, 50.0, 75.0],
        "media_vol_sigma": [1.8, 1.2, 0.9],
    })


@pytest.fixture
def sample_meta_df():
    """Metadata for the 3 synthetic managers."""
    return pd.DataFrame({
        "manager_name": ["Low Performer", "Mid Performer", "High Performer"],
        "slug": ["low-performer", "mid-performer", "high-performer"],
        "age": [56, 47, 41],
        "nationality": ["English", "Spanish", "German"],
        "current_club": ["Club A", "Club B", "Club C"],
        "available": [True, True, True],
        "touchline_bans_3yr": [3, 1, 0],
        "public_disagreements": [2, 0, 0],
        "mid_season_departures": [1, 0, 0],
        "contract_years_remaining": [0.5, 2.0, 3.0],
        "board_backing_score": [3.0, 6.0, 9.0],
        "prev_npxgd_90": [0.05, 0.10, 0.22],
        "prev_ppda": [13.5, 11.0, 8.5],
        "prev_league_pos_pct": [30.0, 50.0, 80.0],
        "squad_value_rank_pct": [60.0, 50.0, 30.0],
        "league_finish_pct": [35.0, 55.0, 85.0],
    })


@pytest.fixture
def sample_config():
    """Minimal scoring config for tests."""
    import yaml
    from pathlib import Path
    config_path = Path(__file__).resolve().parent.parent / "config" / "scoring.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)
