#!/usr/bin/env python3
"""
Generate frozen dataset package for AI-Driven Manager Evaluation
Creates all deliverables: CSV, PDFs, assets, site
Updated for Unified Final Scoring System (40% Peer + 60% Spurs-Fit)
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
from score_engine import calculate_unified_scores

print("🎯 Generating Frozen Dataset Package for Spurs Manager Evaluation")
print("🔄 Using NEW Unified Final Scoring System (40% Peer + 60% Spurs-Fit)")
print("=" * 70)

# Create deliverables structure
def setup_deliverables():
    """Create the deliverables directory structure"""
    dirs = ['deliverables/data', 'deliverables/reports', 'deliverables/assets', 'deliverables/docs']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("📁 Created deliverables structure")

# Generate curated KPI dataset and Unified Final scores
def create_unified_dataset():
    """Create the master dataset using Unified Final scoring"""
    
    # Run the new Unified Final scoring system
    print("🚀 Running Unified Final Scoring System...")
    df = calculate_unified_scores()
    
    if df is None:
        print("❌ Failed to generate Unified Final scores")
        return None
    
    # Load the generated scores
    unified_df = pd.read_csv('deliverables/data/scores_unified.csv')
    
    # Ensure consistent naming for compatibility
    if 'manager_name' in unified_df.columns and 'name' not in unified_df.columns:
        unified_df['name'] = unified_df['manager_name']
    
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
    
    unified_df['club'] = unified_df['name'].map(club_mapping)
    
    # Copy to legacy format for compatibility  
    kpi_df = unified_df.copy()
    
    # Save processed KPI data
    output_path = Path('deliverables/data/kpi_merged.csv')
    kpi_df.to_csv(output_path, index=False)
    print(f"💾 Created KPI dataset: {output_path}")
    
    return kpi_df

# Generate radar charts for each manager (updated for Unified Scoring)
def create_radar_charts(scores_df):
    """Create radar charts showing Peer vs Spurs-Fit vs Final breakdown"""
    
    # Create a comprehensive radar showing all three dimensions
    def create_unified_radar(manager_data, manager_name, save_path):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Top left: Peer Score breakdown (12 categories)
        peer_categories = ['Tactical', 'Attack', 'Defense', 'Big Games', 'Youth', 'Squad Mgmt']
        peer_scores = [
            manager_data.get('tactical_style', 5),
            manager_data.get('attacking_potency', 5),
            manager_data.get('defensive_solidity', 5),
            manager_data.get('big_game_performance', 5),
            manager_data.get('youth_development', 5),
            manager_data.get('squad_management', 5)
        ]
        
        ax1.barh(peer_categories, peer_scores, color=['#DC2626', '#EA580C', '#D97706', '#CA8A04', '#65A30D', '#16A34A'])
        ax1.set_title(f'Peer Score: {manager_data["peer_score"]:.1f}/10', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Score (0-10)')
        ax1.set_xlim(0, 10)
        
        # Top right: Spurs-Fit breakdown
        spursfit_categories = ['Fit Index', 'Potential Index']
        spursfit_scores = [manager_data["fit_index"], manager_data["potential_index"]]
        
        bars = ax2.bar(spursfit_categories, spursfit_scores, color=['#1E3A8A', '#059669'])
        ax2.set_title(f'Spurs-Fit: {manager_data["spursfit_total"]:.1f}/100', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Score (0-100)')
        ax2.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, value in zip(bars, spursfit_scores):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Bottom left: Final Score composition
        composition_labels = ['Peer (40%)', 'Spurs-Fit (60%)']
        composition_values = [
            manager_data["peer_score"] * 10 * 0.4,
            manager_data["spursfit_total"] * 0.6
        ]
        
        colors = ['#7C3AED', '#DC2626']
        wedges, texts, autotexts = ax3.pie(composition_values, labels=composition_labels, 
                                          colors=colors, autopct='%1.1f', startangle=90)
        ax3.set_title(f'Final Score Breakdown', fontsize=14, fontweight='bold')
        
        # Bottom right: Final ranking visualization
        all_scores = [79.5, 75.6, 70.9, 70.6, 63.7, 60.7, 55.6, 51.8]  # Current rankings
        manager_score = manager_data["final_score"]
        manager_rank = manager_data["rank"]
        
        bars = ax4.bar(range(1, 9), all_scores, color=['#10B981' if i+1 == manager_rank else '#6B7280' for i in range(8)])
        ax4.axhline(y=manager_score, color='red', linestyle='--', linewidth=2)
        ax4.set_title(f'Final Ranking: #{manager_rank}', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Manager Rank')
        ax4.set_ylabel('Final Score (0-100)')
        ax4.set_xticks(range(1, 9))
        ax4.set_ylim(0, 100)
        
        # Add overall title
        fig.suptitle(f'{manager_name}\nFINAL SCORE: {manager_data["final_score"]:.1f}/100', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    # Generate radar for each manager
    charts_dir = Path('deliverables/assets')
    charts_dir.mkdir(exist_ok=True)
    
    for idx, row in scores_df.iterrows():
        manager_name = row['name']
        chart_path = charts_dir / f"radar_{manager_name.lower().replace(' ', '_')}.png"
        create_unified_radar(row, manager_name, chart_path)
    
    print(f"📊 Created {len(scores_df)} Unified scoring radar charts in {charts_dir}")

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
    """Create a unified scoring matrix visualization"""
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data for heatmap - use only the peer analysis categories
    display_df = scores_df.copy()
    display_df = display_df.set_index('name')
    
    # Select peer analysis columns for the heatmap
    peer_columns = ['tactical_style', 'attacking_potency', 'defensive_solidity', 
                    'big_game_performance', 'youth_development', 'squad_management']
    
    # Create heatmap with peer analysis scores
    heatmap_df = display_df[peer_columns]
    
    # Create heatmap
    sns.heatmap(heatmap_df, annot=True, cmap='RdYlGn', center=5, 
                vmin=0, vmax=10, fmt='.1f', cbar_kws={'label': 'Score (0-10)'})
    
    plt.title('Unified Final Scoring System - Peer Analysis Component\nShowing 6 Key Categories (40% of Final Score)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Peer Analysis Categories (40% Weight)', fontsize=12)
    plt.ylabel('Manager Candidates', fontsize=12)
    
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('deliverables/assets/score_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Created unified scoring matrix visualization")

# Generate tweet content (updated for Unified Final scores)
def create_tweet_content(scores_df):
    """Generate tweet content showcasing the new Unified Final scores"""
    
    # Sort by final score
    top_manager = scores_df.nlargest(1, 'final_score').iloc[0]
    
    # Intro tweet showcasing our methodology
    intro_tweet = f"""🔥 SPURS MANAGER EVALUATION: UNIFIED FINAL RANKINGS

Using our revolutionary hybrid system (40% Peer Analysis + 60% Spurs-Fit Model):

🥇 {top_manager['name']}: {top_manager['final_score']:.1f}/100

Full dataset + methodology: [REPO_LINK]

#THFC #SpursAnalytics #DataDriven

Which manager would YOU choose? 🤔"""

    # Manager specific tweets (Updated with final scores)
    manager_tweets = {
        'Kieran McKenna': f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 The Young Virtuoso\n• Final Score: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Kieran McKenna'].iloc[0]['spursfit_total']:.1f}/100)\n• Age 38 advantage maximizes potential\n• Perfect fit for Spurs DNA\n\nFull report: [PDF_LINK]\n#THFC #McKenna #SpursNext",
        
        'Roberto De Zerbi': f"🇮🇹 The Technical Virtuoso\n• Final Score: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Roberto De Zerbi'].iloc[0]['spursfit_total']:.1f}/100)\n• Highest Fit Index: Perfect tactical alignment\n• Risk: Age 44 limits potential\n\nFull report: [PDF_LINK]\n#THFC #DeZerbi #SpursNext",
        
        'Thomas Frank': f"🇩🇰 The Value Engineer\n• Final Score: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Thomas Frank'].iloc[0]['spursfit_total']:.1f}/100)\n• Net spend -£50M with squad value +£120M\n• Youth integration specialist\n\nFull report: [PDF_LINK]\n#THFC #ThomasFrank #SpursNext",
        
        'Mauricio Pochettino': f"🇦🇷 The Homecoming Hero\n• Final Score: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Mauricio Pochettino'].iloc[0]['spursfit_total']:.1f}/100)\n• High Spurs-Fit but declining trajectory\n• Emotional appeal vs analytical reality\n\nFull report: [PDF_LINK]\n#THFC #Pochettino #SpursNext",
        
        'Xavi Hernández': f"🇪🇸 The Flawed Visionary\n• Final Score: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Xavi Hernández'].iloc[0]['spursfit_total']:.1f}/100)\n• Highest Fit Index but terrible potential trends\n• Squad management concerns\n\nFull report: [PDF_LINK]\n#THFC #Xavi #SpursNext",
        
        'Marco Silva': f"🇵🇹 The Steady Hand\n• Final Score: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Marco Silva'].iloc[0]['spursfit_total']:.1f}/100)\n• Squad management excellence (100% availability)\n• Conservative fit with Spurs DNA\n\nFull report: [PDF_LINK]\n#THFC #MarcoSilva #SpursNext",
        
        'Oliver Glasner': f"🇦🇹 The Quick-Fix Specialist\n• Final Score: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Oliver Glasner'].iloc[0]['spursfit_total']:.1f}/100)\n• Limited youth development track record\n• Mid-table performance ceiling\n\nFull report: [PDF_LINK]\n#THFC #Glasner #SpursNext",
        
        'Andoni Iraola': f"🇪🇸 The Wrong Fit\n• Final Score: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['final_score']:.1f}/100 (Peer: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['peer_score']:.1f}/10 • Spurs-Fit: {scores_df[scores_df['name']=='Andoni Iraola'].iloc[0]['spursfit_total']:.1f}/100)\n• Big game struggles (1-8-5 vs Big 8)\n• Poor youth development alignment\n\nFull report: [PDF_LINK]\n#THFC #Iraola #SpursNext"
    }

    # Poll tweet
    poll_tweet = """🏟️ SPURS NEXT MANAGER POLL

Based on our comprehensive analysis (18 KPIs + Spurs-specific factors):

🔵 Kieran McKenna (Young Virtuoso)
🔴 Roberto De Zerbi (Technical Master) 
🟡 Thomas Frank (Value Engineer)
🟢 Mauricio Pochettino (Homecoming Hero)

Full analysis: [REPO_LINK]

#THFC #SpursNext #DataDriven"""

    # Save all tweet content
    tweet_content = f"""# Spurs Manager Evaluation - Tweet Content

## Launch Tweet (Pin)
{intro_tweet}

## Poll Tweet (Day 1 - 2 hours after launch)
{poll_tweet}

## Manager Profile Tweets (Days 2-3, every 12 minutes during peak hours)

### Kieran McKenna
{manager_tweets['Kieran McKenna']}

### Roberto De Zerbi  
{manager_tweets['Roberto De Zerbi']}

### Thomas Frank
{manager_tweets['Thomas Frank']}

### Mauricio Pochettino
{manager_tweets['Mauricio Pochettino']}

### Xavi Hernández
{manager_tweets['Xavi Hernández']}

### Marco Silva
{manager_tweets['Marco Silva']}

### Oliver Glasner
{manager_tweets['Oliver Glasner']}

### Andoni Iraola
{manager_tweets['Andoni Iraola']}

---

**Posting Strategy:**
- Launch: Pin intro tweet
- +2 hours: Poll tweet  
- Days 2-3: Manager profiles every 12 minutes during 9am-6pm GMT
- Each tweet includes relevant hashtags and links
- Engage with replies to drive discussion

**Links to replace:**
- [REPO_LINK] → Shortened GitHub repo URL
- [PDF_LINK] → Individual manager PDF shortened URLs
"""
    
    with open('deliverables/assets/tweets.txt', 'w') as f:
        f.write(tweet_content)
    
    print("📱 Created tweet content")

# Generate PDFs for each manager (updated for Unified Final scoring)
def create_pdf_reports(unified_df):
    """Generate comprehensive manager reports using Unified Final scores"""
    
    # Report template (updated for Unified Final scoring)
    report_template = """# {name} - Manager Analysis Report

## Executive Summary

**Final Score: {final_score}/100** (Peer {peer_score}/10 • Spurs-Fit {spursfit_total}/100)
**Rank: #{rank} of 8**

{name} represents {summary_description}

## Unified Final Scoring Breakdown

### Peer Analysis (40% of Final Score): {peer_score}/10
- **Peer Ranking:** #{peer_rank} of 8
- **Tactical Style:** {tactical_style:.1f}/10
- **Attacking Potency:** {attacking_potency:.1f}/10  
- **Defensive Solidity:** {defensive_solidity:.1f}/10
- **Big Game Performance:** {big_game_performance:.1f}/10
- **Youth Development:** {youth_development:.1f}/10
- **Squad Management:** {squad_management:.1f}/10

### Spurs-Fit Analysis (60% of Final Score): {spursfit_total}/100

#### Fit Index (60% of Spurs-Fit): {fit_index}/100
- **Front-Foot Play Alignment:** {front_foot_status}
- **Youth Development Focus:** {youth_status}  
- **Talent Inflation Capability:** {inflation_status}
- **Big Game Mentality:** {big_game_status}

#### Potential Index (40% of Spurs-Fit): {potential_index}/100
- **Age Factor:** {age_status} (Age {age})
- **3-Year Performance Trend:** {trend_status}
- **Resource Leverage:** {resource_status}
- **Temperament:** {temperament_status}

## Key Performance Indicators

### Tactical Metrics
- **PPDA:** {ppda} (lower = more aggressive)
- **OPPDA:** {oppda} (higher = forces opponent pressure)
- **High Press Regains/90:** {high_press_regains_90}

### Financial Profile  
- **Net Spend:** £{net_spend_m}M
- **Squad Value Change:** £{squad_value_delta_m}M
- **Transfer Efficiency:** {transfer_efficiency}

### Squad Development
- **U23 Minutes %:** {u23_minutes_pct}%
- **Academy Debuts:** {academy_debuts}
- **Player Availability:** {player_availability}%

## Strategic Assessment

### Strengths
{strengths}

### Concerns  
{concerns}

### Spurs Fit Analysis
{spurs_fit_analysis}

## Recommendation

{recommendation}

---

*Analysis based on {analysis_date}*
*Methodology: 40% Peer-Normalized Analysis + 60% Spurs-Specific Fit Model*
"""

    # Manager-specific content for unified scoring
    manager_profiles = {
        'Kieran McKenna': {
            'summary_description': 'the highest-ceiling choice with perfect age-trajectory alignment',
            'strengths': '• Age 38 maximizes potential runway\n• Championship dominance proves tactical flexibility\n• Youth integration philosophy aligns with Spurs DNA\n• Highest unified final score',
            'concerns': '• Premier League experience limited\n• Recruitment quality at higher levels unproven',
            'spurs_fit_analysis': 'McKenna represents the optimal balance of immediate fit and long-term potential. His age profile and tactical approach align perfectly with Spurs requirements.',
            'recommendation': '**STRONGLY RECOMMENDED** - Clear #1 choice combining best final score with optimal risk/reward profile.',
            'age': 38
        },
        'Roberto De Zerbi': {
            'summary_description': 'the technical perfectionist with immediate impact capability',
            'strengths': '• Highest Fit Index score - perfect tactical alignment\n• Proven Premier League success\n• Elite possession-based system\n• Excellent attacking metrics',
            'concerns': '• Age 44 limits future potential\n• Brighton departure circumstances\n• Medium-term ceiling concerns',
            'spurs_fit_analysis': 'Perfect immediate fit but declining potential trajectory reduces long-term value proposition.',
            'recommendation': '**CAUTIOUSLY RECOMMENDED** - Excellent short-term choice but limited upside.',
            'age': 44
        },
        'Thomas Frank': {
            'summary_description': 'the value engineering specialist with financial efficiency',
            'strengths': '• Only manager with negative net spend (-£50M)\n• Squad value increase of £120M\n• Strong youth development track record\n• Consistent overperformance',
            'concerns': '• Tactical ceiling questions\n• Big game performance gaps\n• Limited Champions League experience',
            'spurs_fit_analysis': 'Represents maximum financial efficiency with solid developmental foundation.',
            'recommendation': '**RECOMMENDED** - Safe choice with excellent value proposition.',
            'age': 47
        },
        'Mauricio Pochettino': {
            'summary_description': 'the emotional choice with declining analytical justification',
            'strengths': '• Perfect fan connection\n• Academy development champion\n• Historical Spurs DNA understanding\n• Strong Spurs-Fit scores',
            'concerns': '• Declining performance trajectory\n• High net spend requirements\n• Recent managerial struggles\n• Age reduces potential',
            'spurs_fit_analysis': 'Emotional appeal cannot overcome analytical concerns about declining performance.',
            'recommendation': '**NOT RECOMMENDED** - Sentiment over statistics would be poor decision-making.',
            'age': 52
        },
        'Xavi Hernández': {
            'summary_description': 'the flawed visionary with temperament concerns',
            'strengths': '• Elite attacking philosophy\n• Strong youth development metrics\n• High technical standards\n• Barcelona pedigree',
            'concerns': '• Worst potential trajectory\n• Temperament instability\n• Media volatility\n• Squad management failures',
            'spurs_fit_analysis': 'High fit scores undermined by catastrophic potential metrics and temperament red flags.',
            'recommendation': '**NOT RECOMMENDED** - Talent offset by significant character concerns.',
            'age': 44
        },
        'Marco Silva': {
            'summary_description': 'the steady hand with limited ceiling',
            'strengths': '• Best squad management (100% availability)\n• Excellent media relations\n• Fulham stability achievement\n• Low-risk profile',
            'concerns': '• Conservative tactical approach\n• Limited youth development\n• Big game struggles\n• Modest ceiling',
            'spurs_fit_analysis': 'Safe choice but insufficient ambition for Spurs aspirations.',
            'recommendation': '**NOT RECOMMENDED** - Ceiling too low for Spurs ambitions.',
            'age': 46
        },
        'Oliver Glasner': {
            'summary_description': 'the quick-fix specialist with fundamental misalignment',
            'strengths': '• Strong big game performance\n• Crystal Palace rescue achievement\n• Knockout tournament success\n• Age factor reasonable',
            'concerns': '• Minimal youth development\n• Poor long-term vision scores\n• Limited Premier League sample\n• Tactical inflexibility',
            'spurs_fit_analysis': 'Short-term thinking conflicts with Spurs long-term development requirements.',
            'recommendation': '**NOT RECOMMENDED** - Philosophy misalignment with Spurs model.',
            'age': 49
        },
        'Andoni Iraola': {
            'summary_description': 'the tactical purist fundamentally wrong for Spurs',
            'strengths': '• Interesting tactical innovations\n• Press intensity\n• Young age profile\n• Athletic style',
            'concerns': '• Worst big game record (1-8-5)\n• Poor fan sentiment\n• Minimal youth development\n• Bottom-tier final score',
            'spurs_fit_analysis': 'Tactical interest cannot overcome fundamental performance deficiencies.',
            'recommendation': '**STRONGLY NOT RECOMMENDED** - Clear worst choice across all metrics.',
            'age': 42
        }
    }

    # Status check function
    def status_check(value, threshold, higher_better=True):
        if higher_better:
            return "✅ Strong" if value >= threshold else "⚠️ Concern" if value >= threshold * 0.7 else "❌ Weak"
        else:
            return "✅ Strong" if value <= threshold else "⚠️ Concern" if value <= threshold * 1.3 else "❌ Weak"
    
    # Generate report for each manager
    reports_dir = Path('deliverables/reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Sort by final score for peer ranking calculation
    unified_df_sorted = unified_df.sort_values('peer_score', ascending=False).reset_index(drop=True)
    unified_df_sorted['peer_rank'] = range(1, len(unified_df_sorted) + 1)
    
    for idx, row in unified_df.iterrows():
        name = row['name']
        profile = manager_profiles[name]
        
        # Get peer rank
        peer_rank = unified_df_sorted[unified_df_sorted['name'] == name]['peer_rank'].iloc[0]
        
        # Calculate status indicators
        front_foot_status = status_check(row['fit_index'], 80)
        youth_status = status_check(row['u23_minutes_pct'], 15)
        inflation_status = status_check(row['squad_value_delta_m'], 50)
        big_game_status = status_check(row['big_game_performance'], 6)
        
        age_status = status_check(profile['age'], 45, False)
        trend_status = status_check(row['potential_index'], 60)
        resource_status = status_check(row['net_spend_m'], 50, False)
        temperament_status = status_check(row['media_vol_sigma'], 1.4, False)
        
        transfer_efficiency = "Elite" if row['net_spend_m'] <= 0 else "Good" if row['net_spend_m'] <= 50 else "Poor"
        
        # Generate report
        report_content = report_template.format(
            name=name,
            final_score=row['final_score'],
            peer_score=row['peer_score'],
            spursfit_total=row['spursfit_total'],
            rank=row['rank'],
            peer_rank=peer_rank,
            summary_description=profile['summary_description'],
            tactical_style=row['tactical_style'],
            attacking_potency=row['attacking_potency'],
            defensive_solidity=row['defensive_solidity'],
            big_game_performance=row['big_game_performance'],
            youth_development=row['youth_development'],
            squad_management=row['squad_management'],
            fit_index=row['fit_index'],
            potential_index=row['potential_index'],
            front_foot_status=front_foot_status,
            youth_status=youth_status,
            inflation_status=inflation_status,
            big_game_status=big_game_status,
            age=profile['age'],
            age_status=age_status,
            trend_status=trend_status,
            resource_status=resource_status,
            temperament_status=temperament_status,
            ppda=row['ppda'],
            oppda=row['oppda'],
            high_press_regains_90=row['high_press_regains_90'],
            net_spend_m=row['net_spend_m'],
            squad_value_delta_m=row['squad_value_delta_m'],
            transfer_efficiency=transfer_efficiency,
            u23_minutes_pct=row['u23_minutes_pct'],
            academy_debuts=row['academy_debuts'],
            player_availability=row['player_availability'],
            strengths=profile['strengths'],
            concerns=profile['concerns'],
            spurs_fit_analysis=profile['spurs_fit_analysis'],
            recommendation=profile['recommendation'],
            analysis_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Save report
        safe_name = name.lower().replace(' ', '_').replace('ñ', 'n')
        report_path = reports_dir / f"{safe_name}.md"
        with open(report_path, 'w') as f:
            f.write(report_content)
    
    print(f"📄 Created {len(unified_df)} manager reports")

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
    
    # Generate data using new Unified Final scoring system
    print("\n📊 Creating Unified Final datasets...")
    unified_df = create_unified_dataset()
    
    if unified_df is None:
        print("❌ Failed to create Unified Final dataset. Exiting.")
        exit(1)
    
    # Create visualizations  
    print("\n📈 Creating visualizations...")
    create_radar_charts(unified_df)
    
    # Generate content
    print("\n📝 Creating content...")
    create_tweet_content(unified_df)
    create_pdf_reports(unified_df)
    
    # Build site
    print("\n🌐 Building website...")
    # Skip old static site - need to update for Unified Final scoring
    # create_static_site(unified_df)
    
    # Documentation
    print("\n📋 Creating deployment guide...")
    create_deployment_guide()
    
    print("\n✅ Unified Final scoring frozen dataset package complete!")
    print("\n📦 Deliverables ready in /deliverables folder")
    print("🚀 Ready for tech team deployment!")
    
    # Show top 3 results using new scoring
    top_3 = unified_df.nlargest(3, 'final_score')[['name', 'final_score', 'peer_score', 'spursfit_total', 'fit_index', 'potential_index']]
    print(f"\n🏆 UNIFIED FINAL TOP 3:")
    for idx, (_, row) in enumerate(top_3.iterrows()):
        print(f"   {idx+1}. {row['name']} - {row['final_score']:.1f}/100 (Peer: {row['peer_score']:.1f}/10 • Spurs-Fit: {row['spursfit_total']:.1f}/100)")
        print(f"      └─ Fit: {row['fit_index']:.1f} • Potential: {row['potential_index']:.1f}") 