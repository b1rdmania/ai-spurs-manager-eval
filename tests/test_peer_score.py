"""Tests for peer score calculation."""

import pandas as pd
import pytest
from scripts.peer_score import normalize_kpi, calculate_category_score, calculate_peer_scores


class TestNormalizeKPI:
    def test_returns_0_to_1(self, sample_managers_df):
        result = normalize_kpi(sample_managers_df["ppda"])
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_invert_flips_direction(self, sample_managers_df):
        normal = normalize_kpi(sample_managers_df["ppda"], invert=False)
        inverted = normalize_kpi(sample_managers_df["ppda"], invert=True)
        # For PPDA, lower is better, so inverted should have high scores where normal has low
        assert (normal + inverted).mean() == pytest.approx(1.0, abs=0.1)

    def test_identical_values_return_half(self):
        series = pd.Series([5.0, 5.0, 5.0])
        result = normalize_kpi(series)
        assert all(result == 0.5)


class TestCalculateCategoryScore:
    def test_output_range(self, sample_managers_df):
        kpis = {"ppda": {"weight": 1.0, "invert": True}}
        result = calculate_category_score(sample_managers_df, kpis, scale=10.0)
        assert result.min() >= 0.0
        assert result.max() <= 10.0

    def test_empty_kpis_returns_zero(self, sample_managers_df):
        result = calculate_category_score(sample_managers_df, {}, scale=10.0)
        assert all(result == 0.0)

    def test_missing_column_skipped(self, sample_managers_df):
        kpis = {"nonexistent_col": {"weight": 1.0, "invert": False}}
        result = calculate_category_score(sample_managers_df, kpis, scale=10.0)
        assert all(result == 0.0)


class TestCalculatePeerScores:
    def test_all_categories_present(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_peer_scores(df, sample_config)
        for cat in sample_config["peer_categories"]:
            assert f"peer_{cat}" in result.columns

    def test_peer_score_present(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_peer_scores(df, sample_config)
        assert "peer_score" in result.columns

    def test_peer_scores_between_0_and_10(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_peer_scores(df, sample_config)
        assert result["peer_score"].min() >= 0.0
        assert result["peer_score"].max() <= 10.0

    def test_no_nan(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_peer_scores(df, sample_config)
        peer_cols = [c for c in result.columns if c.startswith("peer_")]
        assert not result[peer_cols].isna().any().any()

    def test_high_beats_low(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_peer_scores(df, sample_config)
        high = result.loc[result.index[2], "peer_score"]
        low = result.loc[result.index[0], "peer_score"]
        assert high > low

    def test_weights_sum_to_one(self, sample_config):
        total = sum(c["weight"] for c in sample_config["peer_categories"].values())
        assert total == pytest.approx(1.0, abs=0.01)
