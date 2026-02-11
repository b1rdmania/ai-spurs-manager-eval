"""Spurs-Fit Index — continuous sigmoid scoring for club-specific alignment."""

import math
import pandas as pd


def sigmoid_score(
    value: float,
    center: float,
    steepness: float = 10.0,
    invert: bool = False
) -> float:
    """
    Continuous 0-1 scoring using logistic sigmoid.

    Args:
        value: the raw metric value
        center: the value at which score = 0.5
        steepness: transition sharpness (higher = sharper cutoff)
        invert: True if lower values are better (e.g., PPDA)

    Returns:
        float between 0.0 and 1.0
    """
    if center == 0:
        x = (value - center) * steepness
    else:
        x = (value - center) / abs(center) * steepness

    if invert:
        x = -x

    # Clamp to avoid overflow
    x = max(-20, min(20, x))
    return 1.0 / (1.0 + math.exp(-x))


def calculate_fit_category(
    row: pd.Series,
    metrics_config: dict,
    max_points: float = 25.0
) -> float:
    """
    Calculate a single fit category score for one manager.

    Args:
        row: Series with KPI values
        metrics_config: dict of {metric_name: {center, steepness, invert, weight}}
        max_points: maximum points for this category

    Returns:
        float between 0.0 and max_points
    """
    weighted_sum = 0.0
    total_weight = 0.0

    for metric_name, mcfg in metrics_config.items():
        if metric_name not in row.index:
            continue

        value = row[metric_name]
        if pd.isna(value):
            continue

        score = sigmoid_score(
            value=float(value),
            center=mcfg["center"],
            steepness=mcfg.get("steepness", 10.0),
            invert=mcfg.get("invert", False)
        )

        weight = mcfg.get("weight", 1.0)
        weighted_sum += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight * max_points, 2)


def calculate_fit_index(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate the Spurs-Fit Index for all managers.

    Four categories (front_foot_play, youth_pathway, talent_inflation,
    big_game_mentality), each scored 0-25, totaling 0-100.

    Args:
        df: DataFrame with KPI columns
        config: scoring config dict with 'fit_index' key

    Returns:
        DataFrame with added columns: fit_{category} and fit_index
    """
    df = df.copy()
    fit_cfg = config["fit_index"]

    fit_categories = ["front_foot_play", "youth_pathway", "talent_inflation", "big_game_mentality"]

    for cat_name in fit_categories:
        if cat_name not in fit_cfg:
            continue

        cat_cfg = fit_cfg[cat_name]
        col_name = f"fit_{cat_name}"
        max_pts = cat_cfg.get("max_points", 25.0)

        df[col_name] = df.apply(
            lambda row, mc=cat_cfg["metrics"], mp=max_pts: calculate_fit_category(row, mc, mp),
            axis=1
        )

    # Total fit index = sum of all categories (0-100)
    fit_cols = [f"fit_{c}" for c in fit_categories if f"fit_{c}" in df.columns]
    df["fit_index"] = df[fit_cols].sum(axis=1).round(1)

    return df
