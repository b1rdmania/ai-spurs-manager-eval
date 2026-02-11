import pandas as pd
import numpy as np
import os
import sys

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(__file__))

from fit_index import fit_index
from potential_engine import add_potential

def calculate_peer_scores(df):
    """Calculate the original 12-category peer-normalized scores (0-10 scale)"""
    
    # Category weights (from original weighting.json)
    weights = {
        'tactical_style': 0.12,
        'attacking_potency': 0.11, 
        'defensive_solidity': 0.10,
        'big_game_performance': 0.09,
        'youth_development': 0.08,
        'squad_management': 0.08,
        'transfer_acumen': 0.08,
        'adaptability': 0.07,
        'media_relations': 0.07,
        'fan_connection': 0.07,
        'board_harmony': 0.07,
        'long_term_vision': 0.06
    }
    
    # Calculate tactical style (pressing metrics)
    df['tactical_style'] = (
        (11 - df['ppda'].clip(lower=6, upper=16)) / 5 * 3 +  # PPDA (inverted, lower = better)
        (df['high_press_regains_90'].clip(lower=3, upper=12) - 3) / 9 * 3 +
        (df['oppda'].clip(lower=8, upper=18) - 8) / 10 * 4
    ).clip(0, 10)
    
    # Calculate attacking potency
    df['attacking_potency'] = (
        (df['npxgd_90'].clip(lower=-0.5, upper=0.5) + 0.5) * 4 +
        (df['xg_per_shot'].clip(lower=0.05, upper=0.15) - 0.05) / 0.1 * 3 +
        (df['xg_sequence'].clip(lower=0.05, upper=0.15) - 0.05) / 0.1 * 3
    ).clip(0, 10)
    
    # Calculate defensive solidity (injury management proxy)
    df['defensive_solidity'] = (
        (df['player_availability'].clip(lower=75, upper=95) - 75) / 20 * 10
    ).clip(0, 10)
    
    # Calculate big game performance
    total_big8_games = df['big8_w'] + df['big8_l'] + df['big8_d']
    df['big_game_performance'] = np.where(
        total_big8_games > 0,
        (df['big8_w'] / total_big8_games * 6 + df['ko_win_rate'] / 100 * 4).clip(0, 10),
        (df['ko_win_rate'] / 100 * 10).clip(0, 10)
    )
    
    # Calculate youth development
    df['youth_development'] = (
        (df['u23_minutes_pct'].clip(lower=0, upper=25) / 25 * 6) +
        (df['academy_debuts'].clip(lower=0, upper=15) / 15 * 4)
    ).clip(0, 10)
    
    # Calculate squad management (availability focus)
    df['squad_management'] = (
        df['player_availability'].clip(lower=75, upper=95) - 75
    ) / 20 * 10
    
    # Calculate transfer acumen
    df['transfer_acumen'] = np.where(
        df['net_spend_m'] <= 0,  # Negative or zero net spend
        ((df['squad_value_delta_m'].clip(lower=-50, upper=250) + 50) / 300 * 6 + 4).clip(0, 10),
        ((df['squad_value_delta_m'].clip(lower=-50, upper=250) + 50) / 300 * 8 + 
         (50 - df['net_spend_m'].clip(lower=0, upper=200)) / 200 * 2).clip(0, 10)
    )
    
    # Calculate adaptability (knockout performance)
    df['adaptability'] = (df['ko_win_rate'] / 100 * 10).clip(0, 10)
    
    # Calculate media relations (volatility inverted)
    df['media_relations'] = (
        (2.0 - df['media_vol_sigma'].clip(lower=0.8, upper=2.0)) / 1.2 * 10
    ).clip(0, 10)
    
    # Calculate fan connection
    df['fan_connection'] = (df['fan_sentiment_pct'] / 100 * 10).clip(0, 10)
    
    # Calculate board harmony (media stability + financial efficiency)
    efficiency_score = np.where(
        df['net_spend_m'] <= 0,
        5,
        (50 - df['net_spend_m'].clip(lower=0, upper=200)) / 200 * 3 + 2
    )
    media_score = (2.0 - df['media_vol_sigma'].clip(lower=0.8, upper=2.0)) / 1.2 * 5
    df['board_harmony'] = (efficiency_score + media_score).clip(0, 10)
    
    # Calculate long-term vision (youth + squad value growth)
    df['long_term_vision'] = (
        (df['u23_minutes_pct'].clip(lower=0, upper=25) / 25 * 4) +
        (df['squad_value_delta_m'].clip(lower=-50, upper=250) + 50) / 300 * 6
    ).clip(0, 10)
    
    # Calculate weighted peer score
    peer_score = 0
    for category, weight in weights.items():
        peer_score += df[category] * weight
    
    df['peer_score'] = peer_score.round(1)
    
    return df

def calculate_unified_scores(data_file='manager_data_real.csv', trend_file='data/kpi_trend.csv'):
    """Calculate the unified final scoring system (40% Peer + 60% Spurs-Fit)"""
    
    # Load manager data
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_csv(os.path.join('..', data_file))
    
    # Load trend data
    if os.path.exists(trend_file):
        trend_df = pd.read_csv(trend_file)
    else:
        trend_df = pd.read_csv(os.path.join('..', trend_file))
    
    print(f"📊 Processing {len(df)} managers...")
    
    # Calculate Peer Scores (0-10 scale)
    print("🏟️ Calculating Peer Scores...")
    df = calculate_peer_scores(df)
    
    # Calculate Fit Index (0-100 scale)
    print("🎯 Calculating Fit Index...")
    df = fit_index(df)
    
    # Calculate Potential Index (0-100 scale)
    print("📈 Calculating Potential Index...")
    df = add_potential(df, trend_df)
    
    # Calculate Spurs-Fit Total (60% Fit + 40% Potential)
    print("🔢 Calculating Spurs-Fit Total...")
    df['spursfit_total'] = (0.6 * df['fit_index'] + 0.4 * df['potential_index']).round(1)
    
    # Calculate Final Score (40% Peer + 60% Spurs-Fit)
    print("🏆 Calculating Final Scores...")
    df['final_score'] = (0.4 * df['peer_score'] * 10 + 0.6 * df['spursfit_total']).round(1)
    
    # Sort by final score descending
    df = df.sort_values('final_score', ascending=False).reset_index(drop=True)
    
    # Add rank
    df['rank'] = range(1, len(df) + 1)
    
    # Save results
    output_dir = 'deliverables/data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save unified scores as the main file
    output_file = os.path.join(output_dir, 'scores_unified.csv')
    df.to_csv(output_file, index=False)
    
    # Also save legacy files for backward compatibility
    df.to_csv(os.path.join(output_dir, 'scores_spursfit.csv'), index=False)
    
    print(f"💾 Results saved to {output_file}")
    
    # Display summary
    print("\n🏆 UNIFIED FINAL RANKINGS:")
    print("=" * 80)
    print(f"{'Rank':<4} {'Manager':<20} {'Final':<6} {'Peer':<6} {'Fit':<6} {'Potential':<9}")
    print("=" * 80)
    for _, row in df.iterrows():
        print(f"{int(row['rank']):2d}.  {row['manager_name']:<20} {row['final_score']:5.1f}  {row['peer_score']:4.1f}  {row['fit_index']:5.1f}  {row['potential_index']:7.1f}")
    
    return df

def main():
    """Main execution function"""
    try:
        # Change to parent directory if running from scripts/
        if os.path.basename(os.getcwd()) == 'scripts':
            os.chdir('..')
        
        df = calculate_unified_scores()
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main() 