"""Tests for unified score composition."""

import pytest
from scripts.unified_score import calculate_all_scores


class TestUnifiedScore:
    def test_end_to_end(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        assert "final_score" in result.columns
        assert "rank" in result.columns
        assert len(result) == 3

    def test_final_score_range(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        assert result["final_score"].min() >= 0
        assert result["final_score"].max() <= 100

    def test_ranks_sequential(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        assert result["rank"].tolist() == [1, 2, 3]

    def test_rank_1_has_highest_score(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        rank1 = result[result["rank"] == 1].iloc[0]
        assert rank1["final_score"] == result["final_score"].max()

    def test_formula_composition(self, sample_managers_df, sample_meta_df, sample_config):
        """Verify Final = 40% Peer*10 + 60% SpursFit."""
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        for _, row in result.iterrows():
            expected = 0.4 * row["peer_score"] * 10 + 0.6 * row["spursfit_total"]
            assert row["final_score"] == pytest.approx(expected, abs=0.2)

    def test_spursfit_composition(self, sample_managers_df, sample_meta_df, sample_config):
        """Verify SpursFit = 60% Fit + 40% Potential."""
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        for _, row in result.iterrows():
            expected = 0.6 * row["fit_index"] + 0.4 * row["potential_index"]
            assert row["spursfit_total"] == pytest.approx(expected, abs=0.2)

    def test_all_score_columns_present(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        required = ["peer_score", "fit_index", "potential_index", "spursfit_total", "final_score", "rank"]
        for col in required:
            assert col in result.columns

    def test_no_nan_in_scores(self, sample_managers_df, sample_meta_df, sample_config):
        result = calculate_all_scores(sample_managers_df, sample_meta_df, sample_config)
        score_cols = ["peer_score", "fit_index", "potential_index", "spursfit_total", "final_score"]
        assert not result[score_cols].isna().any().any()
