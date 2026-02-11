"""Pipeline orchestrator — single entry point for the scoring system."""

from pathlib import Path

from scripts.data_loader import load_managers, load_meta, load_config, compute_derived_kpis
from scripts.unified_score import calculate_all_scores
from scripts.export_json import export_scores_json


BASE_DIR = Path(__file__).resolve().parent.parent


def run(
    data_dir: str = None,
    config_path: str = None,
    output_dir: str = None,
    verbose: bool = True
):
    """
    Run the full scoring pipeline.

    Steps:
        1. Load and validate data
        2. Run scoring engine (peer + fit + potential + unified)
        3. Export scores.json for frontend

    Args:
        data_dir: path to data/ directory
        config_path: path to scoring.yaml
        output_dir: path to docs/data/ for JSON output
        verbose: print progress to stdout
    """
    data_path = Path(data_dir) if data_dir else BASE_DIR / "data"
    config_file = Path(config_path) if config_path else BASE_DIR / "config" / "scoring.yaml"
    out_path = Path(output_dir) if output_dir else BASE_DIR / "docs" / "data"

    if verbose:
        print("=" * 60)
        print("SPURS MANAGER EVALUATION v2 — SCORING PIPELINE")
        print("=" * 60)

    # 1. Load
    if verbose:
        print("\n[1/3] Loading data...")
    config = load_config(str(config_file))
    managers_df = load_managers(str(data_path / "managers.csv"))
    meta_df = load_meta(str(data_path / "managers_meta.csv"))
    if verbose:
        print(f"  Loaded {len(managers_df)} managers, {len(managers_df.columns)} KPI columns")

    # 2. Score
    if verbose:
        print("\n[2/3] Running scoring engine...")
    scored_df = calculate_all_scores(managers_df, meta_df, config)

    if verbose:
        print("\n  FINAL RANKINGS:")
        print("  " + "-" * 50)
        for _, row in scored_df.iterrows():
            avail = "✓" if meta_df.loc[meta_df["manager_name"] == row["manager_name"], "available"].iloc[0] else "✗"

            print(f"  #{int(row['rank']):2d}  {row['manager_name']:<25s} {row['final_score']:5.1f}/100  "
                  f"(Peer: {row['peer_score']:.1f} | Fit: {row['fit_index']:.0f} | "
                  f"Pot: {row['potential_index']:.0f}) [{avail}]")
        print("  " + "-" * 50)

    # 3. Export
    if verbose:
        print("\n[3/3] Exporting JSON...")
    export_scores_json(scored_df, meta_df, str(out_path / "scores.json"))

    if verbose:
        print("\nDone.")

    return scored_df


if __name__ == "__main__":
    run()
