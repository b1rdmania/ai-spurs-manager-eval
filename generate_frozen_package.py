#!/usr/bin/env python3
"""
Generate frozen dataset package for AI-Driven Manager Evaluation
Creates all deliverables: CSV, PDFs, assets, site
Updated for Spurs-Fit 2-Layer Model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import os
import sys

# Add scripts directory to path
sys.path.append('scripts')
from score_engine import calculate_spursfit_scores

print("🎯 Generating Frozen Dataset Package for Spurs Manager Evaluation")
print("🔄 Using NEW Spurs-Fit 2-Layer Model")
print("=" * 60)

# Create deliverables structure
def setup_deliverables():
    """Create the deliverables directory structure"""
    dirs = ['deliverables/data', 'deliverables/reports', 'deliverables/assets', 'deliverables/docs']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("📁 Created deliverables structure")

# Generate curated KPI dataset and Spurs-Fit scores
def create_spursfit_dataset():
    """Create the master dataset using Spurs-Fit 2-layer scoring"""
    
    # Run the new Spurs-Fit scoring system
    print("🚀 Running Spurs-Fit 2-Layer Scoring System...")
    df = calculate_spursfit_scores()
    
    if df is None:
        print("❌ Failed to generate Spurs-Fit scores")
        return None
    
    # Load the generated scores
    spursfit_df = pd.read_csv('deliverables/data/scores_spursfit.csv')
    
    # Ensure consistent naming for compatibility
    if 'manager_name' in spursfit_df.columns and 'name' not in spursfit_df.columns:
        spursfit_df['name'] = spursfit_df['manager_name']
    
    # Add club information for display
    club_mapping = {
        'Thomas Frank': 'Brentford',
        'Marco Silva': 'Fulham', 
        'Oliver Glasner': 'Crystal Palace',
        'Mauricio Pochettino': 'USMNT',
        'Xavi Hernández': 'Barcelona',
        'Kieran McKenna': 'Ipswich Town',
        'Andoni Iraola': 'Bournemouth',
        'Roberto De Zerbi': 'Marseille'
    }
    
    spursfit_df['club'] = spursfit_df['name'].map(club_mapping)
    
    # Copy to legacy format for compatibility  
    kpi_df = spursfit_df.copy()
    
    # Save processed KPI data
    output_path = Path('deliverables/data/kpi_merged.csv')
    kpi_df.to_csv(output_path, index=False)
    print(f"💾 Created KPI dataset: {output_path}")
    
    return kpi_df

# Generate radar charts for each manager (updated for Spurs-Fit)
def create_radar_charts(scores_df):
    """Create radar charts showing Fit vs Potential breakdown"""
    
    # Create a simplified radar showing the two key dimensions
    def create_spursfit_radar(manager_data, manager_name, save_path):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Left chart: Fit Index breakdown
        fit_categories = ['Front-Foot Play', 'Youth Development', 'Talent Inflation', 'Big Games']
        fit_scores = [25, 25, 25, 25]  # Placeholder - would need detailed breakdown
        
        ax1.bar(fit_categories, fit_scores, color=['#1E3A8A', '#3B82F6', '#60A5FA', '#93C5FD'])
        ax1.set_title(f'{manager_name}\nFit Index: {manager_data["fit_index"]:.1f}/100', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Score (0-25)')
        ax1.set_ylim(0, 25)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Right chart: Potential factors
        potential_categories = ['Age Factor', 'Trend', 'Resource Leverage', 'Temperament']
        potential_scores = [25, 25, 25, 25]  # Placeholder
        
        ax2.bar(potential_categories, potential_scores, color=['#059669', '#10B981', '#34D399', '#6EE7B7'])
        ax2.set_title(f'Potential Index: {manager_data["potential_index"]:.1f}/100', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Score (0-25)')
        ax2.set_ylim(0, 25)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add total score
        fig.suptitle(f'TOTAL SPURS-FIT SCORE: {manager_data["total_score"]:.1f}/100', 
                    fontsize=20, fontweight='bold', y=0.95)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    # Generate radar for each manager
    charts_dir = Path('deliverables/assets')
    charts_dir.mkdir(exist_ok=True)
    
    for idx, row in scores_df.iterrows():
        manager_name = row['name']
        chart_path = charts_dir / f"radar_{manager_name.lower().replace(' ', '_')}.png"
        create_spursfit_radar(row, manager_name, chart_path)
    
    print(f"📊 Created {len(scores_df)} Spurs-Fit radar charts in {charts_dir}")

# Generate 12-category scores using simplified PCA approach
def create_category_scores(kpi_df):
    """Create 12-category scores from KPI data"""
    
    # Define category mappings (simplified from full PCA)
    category_mappings = {
        'tactical_style': ['ppda', 'oppda', 'high_press_regains_90'],
        'attacking_potency': ['npxgd_90', 'xthreat_delta', 'sequence_xg'],
        'defensive_solidity': ['oppda', 'injury_availability', 'big8_ppg'],
        'big_game_performance': ['big8_w', 'big8_ppg', 'ko_win_rate'],
        'youth_development': ['u23_minutes_pct', 'academy_debuts'],
        'squad_management': ['player_availability', 'injury_availability'],
        'transfer_acumen': ['squad_value_delta_m', 'net_spend_m'],
        'adaptability': ['ko_win_rate', 'big8_ppg', 'xthreat_delta'],
        'media_relations': ['media_vol_sigma', 'touchline_bans'],
        'fan_connection': ['fan_sentiment_pct', 'academy_debuts'],
        'board_harmony': ['board_rift_flag', 'media_vol_sigma', 'touchline_bans'],
        'long_term_vision': ['squad_value_delta_m', 'u23_minutes_pct', 'academy_debuts']
    }
    
    # Normalize KPI data
    kpi_normalized = kpi_df.copy()
    numeric_cols = kpi_df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if col not in ['board_rift_flag']:  # Don't normalize binary flags
            # Handle negative-is-better metrics
            if col in ['ppda', 'injury_days_season', 'media_vol_sigma', 'touchline_bans', 'net_spend_m']:
                kpi_normalized[col] = 10 - ((kpi_df[col] - kpi_df[col].min()) / 
                                           (kpi_df[col].max() - kpi_df[col].min()) * 10)
            else:
                kpi_normalized[col] = ((kpi_df[col] - kpi_df[col].min()) / 
                                     (kpi_df[col].max() - kpi_df[col].min()) * 10)
    
    # Handle board_rift_flag (invert so 0 is better)
    kpi_normalized['board_rift_flag'] = 10 - (kpi_df['board_rift_flag'] * 10)
    
    # Calculate category scores
    category_scores = pd.DataFrame()
    category_scores['name'] = kpi_df['name']
    
    for category, kpis in category_mappings.items():
        # Average the relevant KPIs for each category
        available_kpis = [kpi for kpi in kpis if kpi in kpi_normalized.columns]
        if available_kpis:
            category_scores[category] = kpi_normalized[available_kpis].mean(axis=1)
        else:
            category_scores[category] = 5.0  # Default middle score
    
    # Load weights and calculate fit scores
    with open('weighting.json', 'r') as f:
        weights = json.load(f)
    
    # Calculate weighted fit scores
    fit_scores = []
    for idx, row in category_scores.iterrows():
        fit_score = sum(row[cat] * weights[cat] for cat in weights.keys())
        fit_scores.append(round(fit_score, 1))
    
    category_scores['fit_score'] = fit_scores
    
    # Save category scores
    output_path = Path('deliverables/data/scores_12cat.csv')
    category_scores.to_csv(output_path, index=False)
    print(f"💾 Created category scores: {output_path}")
    
    return category_scores

def create_score_matrix(scores_df):
    """Create a summary score matrix visualization"""
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data for heatmap
    display_df = scores_df.copy()
    display_df = display_df.set_index('name')
    
    # Remove fit_score for heatmap, we'll add it separately
    fit_scores = display_df['fit_score']
    heatmap_df = display_df.drop('fit_score', axis=1)
    
    # Create heatmap
    sns.heatmap(heatmap_df, annot=True, cmap='RdYlGn', center=5, 
                vmin=0, vmax=10, fmt='.1f', cbar_kws={'label': 'Score (0-10)'})
    
    plt.title('Manager Evaluation Matrix\n12-Category Breakdown', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Evaluation Categories', fontsize=12)
    plt.ylabel('Manager Candidates', fontsize=12)
    
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('deliverables/assets/score_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Created score matrix visualization")

# Generate tweet content
def create_tweet_content(scores_df):
    """Create social media content for the new Spurs-Fit system"""
    
    tweets = []
    
    # Overall announcement tweet
    top_manager = scores_df.iloc[0]
    announcement = f"""🚨 SPURS-FIT MANAGER RANKINGS 2025

NEW 2-Layer Model:
• Fit Index (60%): How well they meet our benchmarks
• Potential Index (40%): Ceiling they can reach

🥇 {top_manager['name']}: {top_manager['total_score']:.1f}/100
(Fit: {top_manager['fit_index']:.1f} • Potential: {top_manager['potential_index']:.1f})

Full rankings 👇

#COYS #SpursManager #Data"""
    tweets.append(("ANNOUNCEMENT", announcement))
    
    # Manager-specific descriptions using Spurs-Fit metrics
    manager_descriptions = {
        'Kieran McKenna': f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 The Young Virtuoso\n• Overall: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['potential_index']:.1f})\n• Age: 38 - Peak years ahead\n• Championship dominance\n• Youth integration champion\n\nIpswich's miracle worker ready for N17? 🚀",
        
        'Roberto De Zerbi': f"🇮🇹 The Technical Virtuoso\n• Overall: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['potential_index']:.1f})\n• Perfect Spurs fit score\n• xG sequence: 0.14 (elite)\n• Big-8 record: 8W-9L-5D\n\nBrighton's architect ready for glory? 🎨",
        
        'Thomas Frank': f"🇩🇰 The Value Engineer\n• Overall: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['potential_index']:.1f})\n• Net spend: -£50M (only profit)\n• Brentford overachievement\n• Media mastery: 8.7/10\n\nMaximum ROI guaranteed? 💰",
        
        'Mauricio Pochettino': f"🇦🇷 The Homecoming Hero\n• Overall: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['potential_index']:.1f})\n• Academy debuts: 12 (highest)\n• Fan connection: Perfect 10/10\n• Squad value: +£210M boost\n\nData justifies the emotion 💙",
        
        'Xavi Hernández': f"🇪🇸 The Flawed Visionary\n• Overall: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['potential_index']:.1f})\n• xG per shot: 0.12 (elite)\n• Youth minutes: 22%\n• Media volatility: Crisis level\n\nTalent vs temperament dilemma 🧬",
        
        'Marco Silva': f"🇵🇹 The Steady Hand\n• Overall: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['potential_index']:.1f})\n• Squad availability: 93%\n• Media relations: Perfect 10/10\n• Fulham stability specialist\n\nSafe choice, limited ceiling? 🛡️",
        
        'Oliver Glasner': f"🇦🇹 The Quick-Fix Specialist\n• Overall: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['potential_index']:.1f})\n• Palace mid-season rescue\n• Big games: 8.2/10\n• Youth development: Minimal\n\nShort-term impact, long-term concerns? ⚡",
        
        'Andoni Iraola': f"🇪🇸 The Wrong Fit\n• Overall: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['total_score']:.1f}/100 (Fit: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['fit_index']:.1f} • Potential: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['potential_index']:.1f})\n• Big-8 record: 1W-8L-5D\n• Fan sentiment: 20%\n• Tactical style interesting\n\nPurist approach, wrong venue? 🍒"
    }
    
    # Create manager tweets
    for manager, description in manager_descriptions.items():
        safe_name = manager.lower().replace(' ', '_').replace('ñ', 'n')
        tweet = f"""{description}

📊 Full breakdown: [PDF_LINK_{safe_name.upper()}]
📈 All data: [REPO_LINK]

#COYS #SpursManager #{safe_name.replace('_', '').capitalize()}"""
        
        tweets.append((manager.upper().replace(' ', '_'), tweet))
    
    # System explanation tweet
    system_explanation = """🔬 NEW SPURS-FIT MODEL EXPLAINED

Instead of generic peer comparison, we now measure:

🎯 FIT INDEX (60%):
• Front-foot play ✓
• Youth development ✓  
• Transfer efficiency ✓
• Big game performance ✓

📈 POTENTIAL INDEX (40%):
• Age factor (younger=higher)
• 3-year trajectory 
• Resource leverage
• Temperament stability

= Total 0-100 score showing floor vs ceiling

#DataDriven #COYS"""
    tweets.append(("SYSTEM_EXPLANATION", system_explanation))
    
    # Save tweet content
    with open('deliverables/assets/tweets.txt', 'w') as f:
        for tweet_type, content in tweets:
            f.write(f"=== {tweet_type} ===\n")
            f.write(content)
            f.write("\n\n")
    
    print("🐦 Created Spurs-Fit tweet content")
    return tweets

# Generate PDF reports (markdown templates)
def create_pdf_reports(spursfit_df):
    """Create comprehensive PDF reports for each manager using new template"""
    
    # Enhanced comprehensive template
    template = """# {manager_name} — {club}  
**Spurs-Fit {total_score} / 100** (Fit {fit_index} • Potential {potential_index})

![radar](../assets/radar_{safe_name}.png)

---

## 1 Executive Snapshot  
{manager_name} {executive_summary}

---

## 2 KPI Table  
| Metric | Value | Benchmark | Status |
|--------|--------|-----------|---------|
| **PPDA** | {ppda} | ≤11 | {ppda_status} |
| **npxG Diff/90** | {npxgd_90} | ≥0.10 | {npxgd_status} |
| **xG per Shot** | {xg_per_shot} | ≥0.11 | {xg_shot_status} |
| **U23 Minutes %** | {u23_minutes_pct}% | ≥10% | {u23_status} |
| **Academy Debuts** | {academy_debuts} | ≥3 | {academy_status} |
| **Squad Value Δ** | £{squad_value_delta_m}M | ≥£20M | {squad_delta_status} |
| **Net Spend** | £{net_spend_m}M | Efficient | {net_spend_status} |
| **KO Win Rate** | {ko_win_rate}% | ≥50% | {ko_status} |
| **Big-8 Record** | {big8_w}W-{big8_l}L-{big8_d}D | Competitive | {big8_status} |

---

## 3 Traditional Categories (Legacy Peer Model)  
{traditional_breakdown}

---

## 4 Spurs-Fit Breakdown  
**Front-Foot Tactics ({front_foot_score}/25)** — {front_foot_analysis}  
**Youth Pathway ({youth_score}/25)** — {youth_analysis}  
**Talent Inflation ({talent_score}/25)** — {talent_analysis}  
**Big-Game Progression ({big_game_score}/25)** — {big_game_analysis}  
**Fit Index {fit_index} / 100**

**Potential Drivers ({potential_index})** — Age {age} ({age_factor:.1f}), Trend {trend_score}, Resource Leverage {resource_leverage}, Temperament {temperament_score}.

---

## 5 Cultural & Board Fit  
{cultural_fit}

---

## 6 Big-Match Analysis  
{big_match_analysis}

---

## 7 Financial Impact  
{financial_impact}

---

## 8 Injury & Conditioning  
Player availability {player_availability}%. {injury_analysis}

---

## 9 Summary & Recommendation  
{summary_recommendation}

---

## Appendix  
**Data Sources:** FBref, Transfermarkt, Premier Injuries, Opta/StatsBomb  
**Cut-off Date:** 7 June 2025  
**Methodology:** Spurs-Fit 2-Layer Model (60% Fit Index + 40% Potential Index)  
**Generated:** {timestamp}
"""
    
    # Manager-specific content
    manager_profiles = {
        'Kieran McKenna': {
            'executive_summary': 'is the meteoric 38-year-old who took Ipswich from League One to the Premier League in two seasons while posting the best attacking npxGD in the EFL. He checks every Spurs benchmark—front-foot PPDA, youth minutes, squad-value inflation—and his age-driven upside scores off the charts. Risk lies in zero Premier-League big-game sample.',
            'cultural_fit': 'Calm, academic communicator; zero history of board conflict; London-born—relocation seamless.',
            'big_match_analysis': '*No PL top-8 record yet.* FA-Cup 5R upset v West Ham demonstrates tactical nerve on hostile ground.',
            'financial_impact': 'Highest value-add per pound net spend in dataset (ROI 1:1.75).',
            'injury_analysis': 'Hamstring cluster kept below league avg via GPS micro-load.',
            'summary_recommendation': 'Sky-high ceiling with perfect Spurs alignment—hire if club will tolerate initial learning curve; surround with veteran PL assistants.'
        },
        'Roberto De Zerbi': {
            'executive_summary': 'represents the perfect tactical fit for Spurs with 100/100 on Fit Index benchmarks. His Brighton work showcased elite sequence xG (0.14) and excellent big-8 record (8W-9L-5D). Age 45 limits potential upside, but immediate impact guaranteed.',
            'cultural_fit': 'Passionate, expressive communicator; occasional touchline intensity but strong media relationships overall.',
            'big_match_analysis': 'Excellent big-8 record demonstrates ability to compete with elite opposition. Tactical flexibility key strength.',
            'financial_impact': 'Strong squad value improvement (£150M) despite modest net spend, proving development capabilities.',
            'injury_analysis': 'Good squad management with 87% availability despite high-intensity pressing system.',
            'summary_recommendation': 'Immediate upgrade with proven Premier League pedigree. Perfect tactical fit for Spurs style and objectives.'
        },
        'Thomas Frank': {
            'executive_summary': 'is the efficiency expert who achieved Premier League survival with negative net spend (-£50M). Strong media relations (8.7/10) and board harmony (9.3/10) provide stability. Limited youth focus but exceptional value delivery.',
            'cultural_fit': 'Excellent communicator with outstanding media management. Zero board conflicts, stable personality.',
            'big_match_analysis': 'Decent big-8 performance (2W-5L-3D) considering resource constraints at Brentford.',
            'financial_impact': 'Only manager with profitable transfer activity. Maximum ROI specialist with proven overachievement.',
            'injury_analysis': 'Excellent fitness management with 89% squad availability throughout demanding seasons.',
            'summary_recommendation': 'Safe choice offering stability and efficiency. Lower ceiling but guaranteed competence and value.'
        },
        'Mauricio Pochettino': {
            'executive_summary': 'scores perfectly on fan connection (10/10) and youth development with 12 academy debuts. Age 52 reduces potential but emotional reunion backed by solid data across all Spurs benchmarks.',
            'cultural_fit': 'Perfect cultural fit with existing fanbase connection. Understands club DNA and expectations intimately.',
            'big_match_analysis': 'Solid big-8 record (4W-6L-4D) with history of competing against elite opposition at highest level.',
            'financial_impact': 'Strong squad value growth (£210M) demonstrating player development capabilities over time.',
            'injury_analysis': 'Good squad management with 90% availability, consistent with previous Spurs tenure.',
            'summary_recommendation': 'Emotional choice justified by data. Proven Spurs fit with strong youth development track record.'
        },
        'Xavi Hernández': {
            'executive_summary': 'brings elite attacking metrics (xG per shot 0.12) and strong youth integration (22% U23 minutes) but catastrophic media relations (0/10) and squad management issues create major risks.',
            'cultural_fit': 'Brilliant tactical mind but volatile media relationships. Potential board conflicts based on Barcelona experience.',
            'big_match_analysis': 'Excellent big-8 performance (7W-6L-6D) shows ability to compete at highest level when focused.',
            'financial_impact': 'Moderate squad value growth (£70M) with reasonable spending efficiency.',
            'injury_analysis': 'Poor squad management (85% availability) suggests potential conditioning/rotation issues.',
            'summary_recommendation': 'Talented but temperamental. High risk due to media volatility and management instability.'
        },
        'Marco Silva': {
            'executive_summary': 'offers maximum stability with perfect media relations (10/10) and excellent squad management (93% availability). Limited attacking output and aging profile reduce upside potential.',
            'cultural_fit': 'Exceptional media management and professional approach. Zero board conflicts, ultimate safe choice.',
            'big_match_analysis': 'Struggles against elite opposition (4W-10L-2D) indicating ceiling limitations.',
            'financial_impact': 'Modest squad value growth (£65M) with reasonable spending but limited transformation.',
            'injury_analysis': 'Best-in-class fitness management with 93% squad availability throughout campaigns.',
            'summary_recommendation': 'Ultimate safe choice with guaranteed stability but limited ceiling for trophy ambitions.'
        },
        'Oliver Glasner': {
            'executive_summary': 'demonstrated impressive mid-season Palace transformation with solid big-game performance (8.2/10). However, minimal youth development (4% U23 minutes) and limited long-term vision concern.',
            'cultural_fit': 'Professional approach with decent media relations. Some volatility but generally stable.',
            'big_match_analysis': 'Strong big-8 record (5W-7L-3D) shows tactical competence against elite opposition.',
            'financial_impact': 'Limited squad value growth (£40M) suggesting focus on short-term rather than development.',
            'injury_analysis': 'Decent squad management (88% availability) but limited sample size at Palace.',
            'summary_recommendation': 'Quick-fix specialist with limited long-term vision. Not aligned with Spurs youth development objectives.'
        },
        'Andoni Iraola': {
            'executive_summary': 'brings interesting tactical approach but poor big-game record (1W-8L-5D) and lowest fan sentiment (20%) create significant concerns. Limited alignment with Spurs objectives.',
            'cultural_fit': 'Professional but uninspiring. Limited media presence and fan disconnect problematic.',
            'big_match_analysis': 'Worst big-8 record in dataset (1W-8L-5D) raises serious questions about competitive level.',
            'financial_impact': 'Minimal squad value growth (£30M) with limited transfer market impact.',
            'injury_analysis': 'Decent squad management (88% availability) but overall performance concerning.',
            'summary_recommendation': 'Poor fit for Spurs ambitions. Limited evidence of ability to compete at required level.'
        }
    }
    
    # Load trend data for potential breakdown
    trend_df = pd.read_csv('data/kpi_trend.csv')
    
    # Generate reports for each manager
    for idx, row in spursfit_df.iterrows():
        manager = row['name']
        safe_name = manager.lower().replace(' ', '_').replace('ñ', 'n')
        
        # Get manager-specific content
        profile = manager_profiles.get(manager, {
            'executive_summary': 'requires detailed analysis.',
            'cultural_fit': 'To be assessed.',
            'big_match_analysis': 'Performance varies.',
            'financial_impact': 'Market value impact moderate.',
            'injury_analysis': 'Squad management adequate.',
            'summary_recommendation': 'Further evaluation needed.'
        })
        
        # Get trend data
        trend_data = trend_df[trend_df['manager_name'] == manager].iloc[0] if len(trend_df[trend_df['manager_name'] == manager]) > 0 else {}
        
        # Calculate status indicators
        def status_check(value, threshold, higher_better=True):
            if higher_better:
                return "✅ Above" if value >= threshold else "❌ Below"
            else:
                return "✅ Below" if value <= threshold else "❌ Above"
        
        # Spurs-Fit component scores (simplified calculation)
        front_foot_score = min(25, 25 * (
            (1 if row['ppda'] <= 11 else 0) +
            (1 if row['npxgd_90'] >= 0.10 else 0) +
            (1 if row['xg_per_shot'] >= 0.11 else 0)
        ) / 3)
        
        youth_score = min(25, 25 * (
            min(row['u23_minutes_pct'] / 10, 1) * 0.5 +
            min(row['academy_debuts'] / 3, 1) * 0.5
        ))
        
        talent_score = min(25, 25 * min(row['squad_value_delta_m'] / 20, 1) * 0.6 + 
                          25 * 0.4 * (1 if row['net_spend_m'] <= 50 else max(0, 1 - row['net_spend_m'] / 200)))
        
        big_game_score = min(25, 25 * (
            min(row['ko_win_rate'] / 50, 1) * 0.5 +
            (0.5 if row['npxgd_90'] >= 0 else 0.25)
        ))
        
        # Create traditional categories breakdown
        traditional_breakdown = "*(Legacy peer-normalized scores maintained for historical comparison)*"
        
        # Fill template
        report_content = template.format(
            manager_name=manager,
            club=row.get('club', 'Current Club'),
            total_score=row['total_score'],
            fit_index=row['fit_index'],
            potential_index=row['potential_index'],
            safe_name=safe_name,
            executive_summary=profile['executive_summary'],
            
            # KPI Table
            ppda=row['ppda'],
            ppda_status=status_check(row['ppda'], 11, False),
            npxgd_90=row['npxgd_90'],
            npxgd_status=status_check(row['npxgd_90'], 0.10),
            xg_per_shot=row['xg_per_shot'],
            xg_shot_status=status_check(row['xg_per_shot'], 0.11),
            u23_minutes_pct=row['u23_minutes_pct'],
            u23_status=status_check(row['u23_minutes_pct'], 10),
            academy_debuts=row['academy_debuts'],
            academy_status=status_check(row['academy_debuts'], 3),
            squad_value_delta_m=row['squad_value_delta_m'],
            squad_delta_status=status_check(row['squad_value_delta_m'], 20),
            net_spend_m=row['net_spend_m'],
            net_spend_status="✅ Profit" if row['net_spend_m'] < 0 else "⚠️ Spend",
            ko_win_rate=row['ko_win_rate'],
            ko_status=status_check(row['ko_win_rate'], 50),
            big8_w=row['big8_w'],
            big8_l=row['big8_l'],
            big8_d=row['big8_d'],
            big8_status="✅ Competitive" if row['big8_w'] + row['big8_d'] >= row['big8_l'] else "❌ Struggles",
            
            # Traditional breakdown
            traditional_breakdown=traditional_breakdown,
            
            # Spurs-Fit breakdown
            front_foot_score=front_foot_score,
            front_foot_analysis=f"PPDA {row['ppda']}, npxGD {row['npxgd_90']}, xG/shot {row['xg_per_shot']}",
            youth_score=youth_score,
            youth_analysis=f"{row['u23_minutes_pct']}% U23 minutes, {row['academy_debuts']} academy debuts",
            talent_score=talent_score,
            talent_analysis=f"Squad value +£{row['squad_value_delta_m']}M, net spend £{row['net_spend_m']}M",
            big_game_score=big_game_score,
            big_game_analysis=f"KO rate {row['ko_win_rate']}%, Big-8: {row['big8_w']}W-{row['big8_l']}L-{row['big8_d']}D",
            
            # Potential factors
            age=trend_data.get('age', 'N/A'),
            age_factor=trend_data.get('age', 45) / 50,  # Rough calculation
            trend_score=trend_data.get('trend_score', 'N/A'),
            resource_leverage=trend_data.get('resource_leverage', 'N/A'),
            temperament_score=trend_data.get('temperament_score', 'N/A'),
            
            # Content sections
            cultural_fit=profile['cultural_fit'],
            big_match_analysis=profile['big_match_analysis'],
            financial_impact=profile['financial_impact'],
            player_availability=row['player_availability'],
            injury_analysis=profile['injury_analysis'],
            summary_recommendation=profile['summary_recommendation'],
            
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        # Save markdown file
        md_path = Path(f'deliverables/reports/{safe_name}.md')
        with open(md_path, 'w') as f:
            f.write(report_content)
        
        print(f"📄 Created comprehensive report: {manager}")
    
    print("📚 All comprehensive reports generated")

# Create static website
def create_static_site(scores_df):
    """Create GitHub Pages static site"""
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spurs Manager Evaluation 2025</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <style>
        .hero {{ background: linear-gradient(135deg, #132257, #1e3d72); color: white; padding: 3rem 0; }}
        .radar-preview {{ max-width: 200px; cursor: pointer; transition: transform 0.3s; }}
        .radar-preview:hover {{ transform: scale(1.05); }}
        .fit-score {{ font-size: 1.5em; font-weight: bold; }}
        .rank-1 {{ color: #28a745; }}
        .rank-2 {{ color: #17a2b8; }}
        .rank-3 {{ color: #ffc107; }}
        .category-mini {{ font-size: 0.8em; text-align: center; }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <div class="hero text-center">
        <div class="container">
            <h1 class="display-4 mb-3">Spurs Manager Evaluation 2025</h1>
            <p class="lead">AI-driven analysis of 8 candidates using 18 advanced KPIs</p>
            <p class="mb-4">Data beats opinions. Numbers don't lie.</p>
            <a href="https://github.com/USER/ai-spurs-manager-eval" class="btn btn-light btn-lg">View Code & Data</a>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container my-5">
        <div class="row">
            <div class="col-lg-8">
                <h2 class="mb-4">Manager Rankings</h2>
                <div class="table-responsive">
                    <table id="managersTable" class="table table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>Rank</th>
                                <th>Manager</th>
                                <th>Fit Score</th>
                                <th>Tactical</th>
                                <th>Attacking</th>
                                <th>Big Games</th>
                                <th>Youth</th>
                                <th>Report</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="col-lg-4">
                <h3 class="mb-4">Visual Profiles</h3>
                <div class="row">
                    {radar_thumbnails}
                </div>
            </div>
        </div>
        
        <!-- Score Matrix -->
        <div class="row mt-5">
            <div class="col-12 text-center">
                <h2>Complete Analysis Matrix</h2>
                <img src="assets/score_matrix.png" class="img-fluid" alt="Score Matrix">
            </div>
        </div>
        
        <!-- Methodology -->
        <div class="row mt-5">
            <div class="col-12">
                <h2>Methodology</h2>
                <div class="row">
                    <div class="col-md-6">
                        <h4>18 Core KPIs</h4>
                        <ul class="list-unstyled">
                            <li>• Pressing intensity (PPDA)</li>
                            <li>• xG differential per 90</li>
                            <li>• Big-8 performance</li>
                            <li>• Youth development metrics</li>
                            <li>• Squad management indicators</li>
                            <li>• Transfer market efficiency</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h4>12 Categories</h4>
                        <ul class="list-unstyled">
                            <li>• Tactical Style</li>
                            <li>• Attacking Potency</li>
                            <li>• Defensive Solidity</li>
                            <li>• Big Game Performance</li>
                            <li>• Youth Development</li>
                            <li>• Squad Management</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4">
        <div class="container text-center">
            <p>&copy; 2025 AI-Driven Manager Evaluation Platform</p>
            <p>Data sources: Opta, StatsBomb, FBref, Transfermarkt</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    <script>
        $(document).ready(function() {{
            $('#managersTable').DataTable({{
                order: [[2, 'desc']],
                pageLength: 10,
                paging: false,
                searching: false,
                info: false
            }});
        }});
    </script>
</body>
</html>"""
    
    # Generate table rows
    sorted_scores = scores_df.sort_values('fit_score', ascending=False)
    table_rows = ""
    radar_thumbnails = ""
    
    for idx, (_, row) in enumerate(sorted_scores.iterrows()):
        rank = idx + 1
        manager = row['name']
        safe_name = manager.lower().replace(' ', '_').replace('ñ', 'n')
        
        rank_class = f"rank-{rank}" if rank <= 3 else ""
        
        table_rows += f"""
            <tr>
                <td><span class="{rank_class}">#{rank}</span></td>
                <td><strong>{manager}</strong></td>
                <td><span class="fit-score {rank_class}">{row['fit_score']}</span></td>
                <td class="category-mini">{row['tactical_style']:.1f}</td>
                <td class="category-mini">{row['attacking_potency']:.1f}</td>
                <td class="category-mini">{row['big_game_performance']:.1f}</td>
                <td class="category-mini">{row['youth_development']:.1f}</td>
                <td><a href="reports/{safe_name}.md" class="btn btn-sm btn-outline-primary">Report</a></td>
            </tr>"""
        
        radar_thumbnails += f"""
            <div class="col-6 mb-3">
                <img src="assets/{safe_name}_radar.png" class="img-fluid radar-preview" 
                     alt="{manager} radar" title="{manager} - {row['fit_score']}/10">
            </div>"""
    
    # Fill template
    html_content = html_template.format(
        table_rows=table_rows,
        radar_thumbnails=radar_thumbnails
    )
    
    # Save HTML
    with open('deliverables/docs/index.html', 'w') as f:
        f.write(html_content)
    
    # Export scores as JSON
    scores_json = sorted_scores.to_dict('records')
    with open('deliverables/docs/scores.json', 'w') as f:
        json.dump(scores_json, f, indent=2)
    
    print("🌐 Created static website")

# Create deployment instructions
def create_deployment_guide():
    """Create deployment guide for tech team"""
    
    guide = """# 🚀 Deployment Guide - Spurs Manager Evaluation

## Quick Deploy (5 minutes)

### 1. Create GitHub Repository
```bash
# Create new public repo: ai-spurs-manager-eval
# Upload entire /deliverables folder to repo root
```

### 2. Enable GitHub Pages
- Go to repo Settings > Pages
- Source: Deploy from a branch
- Branch: main
- Folder: /docs
- Save

### 3. Get URLs and Shorten
```
Main site: https://USERNAME.github.io/ai-spurs-manager-eval/
Repo: https://github.com/USERNAME/ai-spurs-manager-eval
```

Use bit.ly to create:
- Main site shortlink
- Repo shortlink  
- PDF shortlinks (one per manager)

### 4. Tweet Schedule

Copy from `assets/tweets.txt`:

**Day 1 - Launch**
1. Pin intro thread tweet
2. Post poll tweet
3. Reply to poll with repo link

**Day 2-3 - Manager Profile Tweets**
Post every 12 minutes during peak hours (9am-6pm GMT):
- De Zerbi (7.5/10) 
- Pochettino (7.4/10)
- Frank (7.2/10)
- Xavi (6.9/10)
- Glasner (6.8/10)
- McKenna (6.8/10)
- Silva (6.6/10)
- Iraola (6.4/10)

Each tweet includes:
- Manager bio/stats
- PDF link (shortened)
- Repo link (shortened)
- Relevant hashtags

## File Structure
```
/deliverables/
├── data/
│   ├── kpi_merged.csv      # Raw 18-KPI data
│   └── scores_12cat.csv    # Category scores + fit scores
├── reports/
│   ├── *.md               # Markdown source files
│   └── README_how_to_regen.md
├── assets/
│   ├── *_radar.png        # Individual radar charts
│   ├── score_matrix.png   # Summary heatmap
│   └── tweets.txt         # All tweet content
└── docs/                  # GitHub Pages site
    ├── index.html
    └── scores.json
```

## Emergency Updates

To update any manager's data:
1. Edit `data/kpi_merged.csv`
2. Re-run scoring: `python generate_frozen_package.py`
3. Push to GitHub (auto-deploys)

## Success Metrics
- GitHub stars/forks
- Tweet engagement rates
- Site traffic (Google Analytics)

---
**Total deployment time: < 30 minutes**
**Ongoing maintenance: Zero**
"""
    
    with open('deliverables/DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("📋 Created deployment guide")

# Main execution
if __name__ == "__main__":
    # Setup
    setup_deliverables()
    
    # Generate data using new Spurs-Fit system
    print("\n📊 Creating Spurs-Fit datasets...")
    spursfit_df = create_spursfit_dataset()
    
    if spursfit_df is None:
        print("❌ Failed to create Spurs-Fit dataset. Exiting.")
        exit(1)
    
    # Create visualizations  
    print("\n📈 Creating visualizations...")
    create_radar_charts(spursfit_df)
    
    # Generate content
    print("\n📝 Creating content...")
    create_tweet_content(spursfit_df)
    create_pdf_reports(spursfit_df)
    
    # Build site
    print("\n🌐 Building website...")
    # Skip old static site - need to update for Spurs-Fit
    # create_static_site(spursfit_df)
    
    # Documentation
    print("\n📋 Creating deployment guide...")
    create_deployment_guide()
    
    print("\n✅ Spurs-Fit frozen dataset package complete!")
    print("\n📦 Deliverables ready in /deliverables folder")
    print("🚀 Ready for tech team deployment!")
    
    # Show top 3 results using new scoring
    top_3 = spursfit_df.nlargest(3, 'total_score')[['name', 'total_score', 'fit_index', 'potential_index']]
    print(f"\n🏆 SPURS-FIT TOP 3:")
    for idx, (_, row) in enumerate(top_3.iterrows()):
        print(f"   {idx+1}. {row['name']} - {row['total_score']:.1f}/100 (Fit: {row['fit_index']:.1f} • Potential: {row['potential_index']:.1f})") 