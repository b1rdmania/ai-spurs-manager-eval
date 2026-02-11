"""Peer score calculation — 9 categories, each scored 0-10."""

import numpy as np
import pandas as pd


def normalize_kpi(series: pd.Series, invert: bool = False) -> pd.Series:
    """
    Normalize a KPI series to 0-1 using min-max scaling against the peer group.
    Uses p5/p95 clipping to reduce outlier influence.
    If invert=True, lower values score higher.
    """
    p5 = series.quantile(0.05)
    p95 = series.quantile(0.95)

    # Avoid division by zero when all values are identical
    if p95 == p5:
        return pd.Series(0.5, index=series.index)

    clipped = series.clip(lower=p5, upper=p95)
    normalized = (clipped - p5) / (p95 - p5)

    if invert:
        normalized = 1.0 - normalized

    return normalized


def calculate_category_score(
    df: pd.DataFrame,
    kpis: dict,
    scale: float = 10.0
) -> pd.Series:
    """
    Calculate a single peer category score for all managers.

    Args:
        df: DataFrame with KPI columns
        kpis: dict of {kpi_name: {weight, invert, derived?}}
        scale: max score (default 10.0)

    Returns:
        Series of scores (0 to scale)
    """
    weighted_sum = pd.Series(0.0, index=df.index)
    total_weight = 0.0

    for kpi_name, kpi_cfg in kpis.items():
        if kpi_name not in df.columns:
            continue

        weight = kpi_cfg.get("weight", 1.0)
        invert = kpi_cfg.get("invert", False)

        normalized = normalize_kpi(df[kpi_name], invert=invert)
        weighted_sum += normalized * weight
        total_weight += weight

    if total_weight == 0:
        return pd.Series(0.0, index=df.index)

    return (weighted_sum / total_weight * scale).round(2)


def calculate_peer_scores(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate all 9 peer category scores and the weighted average.

    Args:
        df: DataFrame with all KPI columns (including derived)
        config: scoring config dict with 'peer_categories' key

    Returns:
        DataFrame with added columns: peer_{category} and peer_score
    """
    df = df.copy()
    categories = config["peer_categories"]

    weighted_total = pd.Series(0.0, index=df.index)
    total_weight = 0.0

    for cat_name, cat_cfg in categories.items():
        col_name = f"peer_{cat_name}"
        score = calculate_category_score(df, cat_cfg["kpis"])
        df[col_name] = score

        weight = cat_cfg["weight"]
        weighted_total += score * weight
        total_weight += weight

    # Weighted average across categories (should sum to ~1.0)
    df["peer_score"] = (weighted_total / total_weight).round(2)

    return df
