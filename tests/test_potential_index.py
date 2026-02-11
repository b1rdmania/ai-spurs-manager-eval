"""Tests for potential index calculation."""

import pytest
from scripts.potential_index import (
    age_factor,
    calculate_trend_score,
    calculate_temperament_score,
    calculate_resource_leverage,
    calculate_potential_index,
)


class TestAgeFactor:
    def test_peak_at_43(self):
        scores = {age: age_factor(age) for age in range(35, 60)}
        assert max(scores, key=scores.get) == 43

    def test_symmetric_around_peak(self):
        s38 = age_factor(38)
        s48 = age_factor(48)
        # Both 5 years from peak, should be similar
        assert abs(s38 - s48) < 0.01

    def test_young_above_old(self):
        assert age_factor(39) > age_factor(55)

    def test_output_range(self):
        for age in range(30, 65):
            score = age_factor(age)
            assert 0.0 <= score <= 1.0

    def test_age_43_is_max(self):
        assert age_factor(43) == pytest.approx(1.0, abs=0.001)


class TestTrendScore:
    def test_stable_returns_half(self):
        score = calculate_trend_score(0.1, 0.1, 10.0, 10.0, 50.0, 50.0)
        assert score == pytest.approx(0.5, abs=0.01)

    def test_improving_above_half(self):
        score = calculate_trend_score(0.2, 0.1, 9.0, 11.0, 70.0, 50.0)
        assert score > 0.5

    def test_declining_below_half(self):
        score = calculate_trend_score(0.05, 0.15, 12.0, 10.0, 30.0, 50.0)
        assert score < 0.5

    def test_output_range(self):
        score = calculate_trend_score(0.5, -0.3, 6.0, 14.0, 90.0, 10.0)
        assert 0.0 <= score <= 1.0


class TestTemperamentScore:
    def test_clean_record_high(self):
        score = calculate_temperament_score(0, 0, 0, 3.0)
        assert score > 0.9

    def test_problematic_record_low(self):
        score = calculate_temperament_score(3, 2, 1, 0.0)
        assert score < 0.4

    def test_output_range(self):
        for bans in range(5):
            for disputes in range(4):
                score = calculate_temperament_score(bans, disputes, 0, 2.0)
                assert 0.0 <= score <= 1.0


class TestResourceLeverage:
    def test_even_returns_half(self):
        score = calculate_resource_leverage(50.0, 50.0)
        assert score == pytest.approx(0.5, abs=0.01)

    def test_overperformer_above_half(self):
        score = calculate_resource_leverage(80.0, 30.0)
        assert score > 0.5

    def test_underperformer_below_half(self):
        score = calculate_resource_leverage(20.0, 70.0)
        assert score < 0.5


class TestPotentialIndex:
    def test_output_range(self, sample_managers_df, sample_meta_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_potential_index(df, sample_meta_df, sample_config)
        assert result["potential_index"].min() >= 0
        assert result["potential_index"].max() <= 100

    def test_components_present(self, sample_managers_df, sample_meta_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_potential_index(df, sample_meta_df, sample_config)
        for col in ["pot_age", "pot_trend", "pot_leverage", "pot_temperament", "potential_index"]:
            assert col in result.columns

    def test_no_nan(self, sample_managers_df, sample_meta_df, sample_config):
        from scripts.data_loader import compute_derived_kpis
        df = compute_derived_kpis(sample_managers_df)
        result = calculate_potential_index(df, sample_meta_df, sample_config)
        assert not result["potential_index"].isna().any()
