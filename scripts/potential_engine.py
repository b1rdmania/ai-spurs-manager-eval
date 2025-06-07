import yaml
import pandas as pd
import os

def load_weights():
    weights_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'potential_weights.yaml')
    with open(weights_path, 'r') as f:
        return yaml.safe_load(f)

def potential_index(row, w):
    """Calculate potential index based on age, trend, leverage, and temperament"""
    # Age factor (reverse-scaled: younger = higher potential)
    age_score = max(0, min(1, (60 - row['age']) / 25))  # Peak potential at ~35, declining after
    
    # Trend factor (direct from 3-yr CAGR)
    trend_score = row['trend_score']
    
    # Resource leverage (how well they use resources)
    leverage_score = row['resource_leverage']
    
    # Temperament (stability, board relations)
    temperament_score = row['temperament_score']
    
    # Weighted combination
    potential = 100 * (
        w['age_factor'] * age_score +
        w['trend_factor'] * trend_score +
        w['resource_leverage'] * leverage_score +
        w['temperament_factor'] * temperament_score
    )
    
    return round(potential, 1)

def add_potential(df, trend_df):
    """Add potential index to manager dataframe"""
    w = load_weights()
    
    # Merge with trend data
    df_merged = df.merge(trend_df, on='manager_name', how='left')
    
    # Calculate potential index for each manager
    potential_scores = []
    for _, row in df_merged.iterrows():
        pot_score = potential_index(row, w)
        potential_scores.append(pot_score)
    
    df_merged['potential_index'] = potential_scores
    
    # Return only original columns plus new potential_index
    original_cols = list(df.columns) + ['potential_index']
    return df_merged[original_cols]

def test_potential_engine():
    """Test the potential engine with sample data"""
    # Create test manager data
    manager_data = pd.DataFrame({
        'manager_name': ['Young Manager', 'Experienced Manager'],
        'some_stat': [1, 2]
    })
    
    # Create test trend data
    trend_data = pd.DataFrame({
        'manager_name': ['Young Manager', 'Experienced Manager'],
        'age': [40, 55],
        'trend_score': [0.8, 0.3],
        'resource_leverage': [0.7, 0.9],
        'temperament_score': [0.9, 0.8]
    })
    
    result = add_potential(manager_data, trend_data)
    
    # Young manager should have higher potential
    young_potential = result[result['manager_name'] == 'Young Manager']['potential_index'].iloc[0]
    exp_potential = result[result['manager_name'] == 'Experienced Manager']['potential_index'].iloc[0]
    
    assert young_potential > exp_potential, f"Young manager potential ({young_potential}) should be higher than experienced ({exp_potential})"
    assert 0 <= young_potential <= 100, f"Potential score should be 0-100, got {young_potential}"
    
    print(f"✅ Test passed: Young={young_potential}, Experienced={exp_potential}")
    return True

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        test_potential_engine()
    else:
        print("Use --test flag to run tests") 