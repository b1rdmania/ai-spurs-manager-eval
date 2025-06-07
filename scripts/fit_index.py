import yaml
import pandas as pd
import sys
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'benchmarks.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def calc_front_foot(row, cfg):
    """Calculate front-foot attacking score (0-25 points)"""
    hits = 0
    hits += int(row['ppda'] <= cfg['front_foot']['ppda_max'])
    hits += int(row['npxgd_90'] >= cfg['front_foot']['npxgd90_min'])
    hits += int(row['xg_per_shot'] >= cfg['front_foot']['xg_per_shot_min'])
    return 25 * hits / 3

def calc_youth(row, cfg):
    """Calculate youth development score (0-25 points)"""
    u23_score = min(row['u23_minutes_pct'] / cfg['youth']['u23_min_pct'], 1) * 0.5
    academy_score = min(row['academy_debuts'] / cfg['youth']['academy_debuts_min'], 1) * 0.5
    return 25 * (u23_score + academy_score)

def calc_talent_inflation(row, cfg):
    """Calculate talent development/transfer efficiency score (0-25 points)"""
    # Squad value growth efficiency
    squad_eff = min(row['squad_value_delta_m'] / cfg['talent_inflation']['squad_delta_min'], 1) * 0.6
    
    # Net spend efficiency (lower net spend = better, capped at reasonable range)
    net_spend_eff = 0.4
    if row['net_spend_m'] <= 0:  # Negative spend = perfect efficiency
        net_spend_eff = 0.4
    elif row['net_spend_m'] <= 50:  # Reasonable spend
        net_spend_eff = 0.4 * (1 - row['net_spend_m'] / 100)
    else:  # High spend = lower efficiency
        net_spend_eff = 0.4 * max(0, 1 - row['net_spend_m'] / 200)
    
    return 25 * (squad_eff + net_spend_eff)

def calc_big_games(row, cfg):
    """Calculate big game performance score (0-25 points)"""
    ko_score = min(row['ko_win_rate'] / cfg['big_games']['ko_win_rate_min'], 1) * 0.5
    
    # Big 8 performance based on npxG differential
    big8_score = 0.5
    if row['npxgd_90'] >= cfg['big_games']['big8_npxgd_min']:
        big8_score = 0.5 * min(row['npxgd_90'] / 0.2, 1)  # Scale to 0.2 as good performance
    
    return 25 * (ko_score + big8_score)

def fit_index(df):
    """Calculate Spurs-specific fit index for all managers"""
    cfg = load_config()
    scores = []
    
    for _, row in df.iterrows():
        front_foot_score = calc_front_foot(row, cfg)
        youth_score = calc_youth(row, cfg)
        talent_score = calc_talent_inflation(row, cfg)
        big_game_score = calc_big_games(row, cfg)
        
        total_fit = front_foot_score + youth_score + talent_score + big_game_score
        scores.append(round(total_fit, 1))
    
    df['fit_index'] = scores
    return df

def test_fit_index():
    """Test function with assertions"""
    # Create test data
    test_data = {
        'name': ['Test Manager'],
        'ppda': [10.0],  # Good (≤11)
        'npxgd_90': [0.15],  # Good (≥0.10)
        'xg_per_shot': [0.12],  # Good (≥0.11)
        'u23_minutes_pct': [15],  # Good (≥10)
        'academy_debuts': [5],  # Good (≥3)
        'squad_value_delta_m': [30],  # Good (≥20)
        'net_spend_m': [25],  # Reasonable
        'ko_win_rate': [60],  # Good (≥50)
    }
    
    test_df = pd.DataFrame(test_data)
    result_df = fit_index(test_df)
    
    # Should score well across all categories
    fit_score = result_df['fit_index'].iloc[0]
    assert fit_score > 70, f"Expected fit score > 70, got {fit_score}"
    assert fit_score <= 100, f"Expected fit score ≤ 100, got {fit_score}"
    
    print(f"✅ Test passed: Fit score = {fit_score}")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        test_fit_index()
    else:
        print("Use --test flag to run tests") 