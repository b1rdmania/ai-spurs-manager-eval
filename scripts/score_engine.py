import pandas as pd
import os
import sys

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(__file__))

from fit_index import fit_index
from potential_engine import add_potential

def calculate_spursfit_scores(data_file='manager_data_real.csv', trend_file='data/kpi_trend.csv'):
    """Calculate the new Spurs-Fit 2-layer scoring system"""
    
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
    
    # Calculate Fit Index (60% weight)
    print("🎯 Calculating Fit Index...")
    df = fit_index(df)
    
    # Calculate Potential Index (40% weight)
    print("📈 Calculating Potential Index...")
    df = add_potential(df, trend_df)
    
    # Calculate combined Total Score
    print("🔢 Calculating Total Scores...")
    df['total_score'] = (0.6 * df['fit_index'] + 0.4 * df['potential_index']).round(1)
    
    # Sort by total score descending
    df = df.sort_values('total_score', ascending=False).reset_index(drop=True)
    
    # Add rank
    df['rank'] = range(1, len(df) + 1)
    
    # Save results
    output_dir = 'deliverables/data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'scores_spursfit.csv')
    df.to_csv(output_file, index=False)
    
    print(f"💾 Results saved to {output_file}")
    
    # Display summary
    print("\n🏆 SPURS-FIT RANKINGS:")
    print("=" * 70)
    for _, row in df.iterrows():
        print(f"{int(row['rank']):2d}. {row['manager_name']:20s} | Total: {row['total_score']:5.1f} (Fit: {row['fit_index']:4.1f} • Potential: {row['potential_index']:4.1f})")
    
    return df

def main():
    """Main execution function"""
    try:
        # Change to parent directory if running from scripts/
        if os.path.basename(os.getcwd()) == 'scripts':
            os.chdir('..')
        
        df = calculate_spursfit_scores()
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main() 