"""Tests for data loading and validation."""

import pytest
import pandas as pd
from scripts.data_loader import validate_managers, validate_meta, compute_derived_kpis, REQUIRED_KPI_COLUMNS


class TestValidateManagers:
    def test_valid_data_no_errors(self, sample_managers_df):
        errors = validate_managers(sample_managers_df)
        assert errors == []

    def test_missing_column(self, sample_managers_df):
        df = sample_managers_df.drop(columns=["ppda"])
        errors = validate_managers(df)
        assert any("Missing columns" in e for e in errors)

    def test_duplicate_managers(self, sample_managers_df):
        df = pd.concat([sample_managers_df, sample_managers_df.iloc[:1]])
        errors = validate_managers(df)
        assert any("Duplicate" in e for e in errors)

    def test_null_values(self, sample_managers_df):
        df = sample_managers_df.copy()
        df.loc[0, "ppda"] = None
        errors = validate_managers(df)
        assert any("null" in e for e in errors)

    def test_out_of_range(self, sample_managers_df):
        df = sample_managers_df.copy()
        df.loc[0, "ppda"] = 100.0  # Way out of range
        errors = validate_managers(df)
        assert any("outside range" in e for e in errors)


class TestValidateMeta:
    def test_valid_meta_no_errors(self, sample_meta_df):
        errors = validate_meta(sample_meta_df)
        assert errors == []

    def test_unreasonable_age(self, sample_meta_df):
        df = sample_meta_df.copy()
        df.loc[0, "age"] = 15
        errors = validate_meta(df)
        assert any("age" in e for e in errors)


class TestComputeDerivedKPIs:
    def test_big6_win_pct_added(self, sample_managers_df):
        result = compute_derived_kpis(sample_managers_df)
        assert "big6_win_pct" in result.columns

    def test_big6_xgd_added(self, sample_managers_df):
        result = compute_derived_kpis(sample_managers_df)
        assert "big6_xgd" in result.columns

    def test_big6_win_pct_range(self, sample_managers_df):
        result = compute_derived_kpis(sample_managers_df)
        assert result["big6_win_pct"].min() >= 0
        assert result["big6_win_pct"].max() <= 100
