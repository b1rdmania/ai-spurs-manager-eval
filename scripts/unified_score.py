"""Unified Final Score — combines Peer Analysis and Spurs-Fit Model."""

import pandas as pd

from scripts.data_loader import load_managers, load_meta, load_config, compute_derived_kpis
from scripts.peer_score import calculate_peer_scores
from scripts.fit_index import calculate_fit_index
from scripts.potential_index import calculate_potential_index


def calculate_all_scores(
    managers_df: pd.DataFrame,
    meta_df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Run the complete scoring pipeline.

    Formula:
        Spurs-Fit Total = (Fit Index * 0.60) + (Potential Index * 0.40)
        Final Score = (Peer Score * 10 * 0.40) + (Spurs-Fit Total * 0.60)

    Args:
        managers_df: DataFrame with KPI columns
        meta_df: DataFrame with metadata
        config: scoring configuration dict

    Returns:
        DataFrame with all scores, ranked by final_score descending
    """
    # Compute derived KPIs
    df = compute_derived_kpis(managers_df)

    # Peer scores (9 categories, 0-10 each)
    df = calculate_peer_scores(df, config)

    # Fit index (4 categories, 0-25 each, total 0-100)
    df = calculate_fit_index(df, config)

    # Potential index (0-100)
    df = calculate_potential_index(df, meta_df, config)

    # Spurs-Fit Total
    fit_comp = config["fit_index"]["composition"]
    df["spursfit_total"] = (
        fit_comp["fit_weight"] * df["fit_index"]
        + fit_comp["potential_weight"] * df["potential_index"]
    ).round(1)

    # Final Score
    final_cfg = config["final_score"]
    df["final_score"] = (
        final_cfg["peer_weight"] * df["peer_score"] * 10
        + final_cfg["spursfit_weight"] * df["spursfit_total"]
    ).round(1)

    # Rank
    df = df.sort_values("final_score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    return df


def run_from_files(
    managers_csv: str = None,
    meta_csv: str = None,
    config_path: str = None
) -> pd.DataFrame:
    """Convenience: load files and run scoring."""
    config = load_config(config_path)
    managers_df = load_managers(managers_csv)
    meta_df = load_meta(meta_csv)
    return calculate_all_scores(managers_df, meta_df, config)
