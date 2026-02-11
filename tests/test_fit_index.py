"""Tests for fit index calculation."""

import pytest
from scripts.fit_index import sigmoid_score, calculate_fit_category, calculate_fit_index
import pandas as pd


class TestSigmoidScore:
    def test_output_range(self):
        for val in [-100, -10, 0, 5, 10, 100]:
            result = sigmoid_score(val, center=10.0, steepness=5)
            assert 0.0 <= result <= 1.0

    def test_center_gives_approximately_half(self):
        result = sigmoid_score(10.0, center=10.0, steepness=5)
        assert result == pytest.approx(0.5, abs=0.01)

    def test_invert_flips(self):
        normal = sigmoid_score(8.0, center=10.0, steepness=5, invert=False)
        inverted = sigmoid_score(8.0, center=10.0, steepness=5, invert=True)
        # Below center: normal < 0.5, inverted > 0.5
        assert normal < 0.5
        assert inverted > 0.5

    def test_higher_steepness_sharper(self):
        soft = sigmoid_score(12.0, center=10.0, steepness=3)
        sharp = sigmoid_score(12.0, center=10.0, steepness=15)
        # Both > 0.5, but sharper should be closer to 1
        assert sharp > soft

    def test_no_cliff(self):
        """Small input changes produce small output changes."""
        values = [9.0, 9.5, 10.0, 10.5, 11.0]
        scores = [sigmoid_score(v, center=10.0, steepness=8) for v in values]
        for i in range(len(scores) - 1):
            assert abs(scores[i] - scores[i+1]) < 0.3  # No jump > 0.3


class TestCalculateFitIndex:
    def test_fit_index_range(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_fit_index(df, sample_config)
        assert result["fit_index"].min() >= 0
        assert result["fit_index"].max() <= 100

    def test_four_categories_present(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_fit_index(df, sample_config)
        for cat in ["front_foot_play", "youth_pathway", "talent_inflation", "big_game_mentality"]:
            assert f"fit_{cat}" in result.columns

    def test_each_category_max_25(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_fit_index(df, sample_config)
        for cat in ["front_foot_play", "youth_pathway", "talent_inflation", "big_game_mentality"]:
            col = f"fit_{cat}"
            assert result[col].max() <= 25.0
            assert result[col].min() >= 0.0

    def test_no_nan(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_fit_index(df, sample_config)
        assert not result["fit_index"].isna().any()

    def test_high_performer_scores_higher(self, sample_managers_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_fit_index(df, sample_config)
        high = result.loc[2, "fit_index"]
        low = result.loc[0, "fit_index"]
        assert high > low
