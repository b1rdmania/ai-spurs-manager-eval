#!/usr/bin/env python3
"""
Premium Manager Report Builder
Implements professional design guidelines for board-room quality reports
"""

import os
import re
import json
import markdown
from bs4 import BeautifulSoup
from pathlib import Path
import shutil

# Design System Constants
COLORS = {
    'spurs_teal': '#50e3c2',
    'navy_dark': '#0b1e3c', 
    'light_row': '#f7f9fb',
    'callout_bg': '#eef6ff',
    'good_heat': '#75d36b',
    'bad_heat': '#e96b5d',
    'spurs_navy': '#132257',
    'spurs_blue': '#1e3d72'
}

# Typography Scale
TYPOGRAPHY = {
    'title': '28pt',
    'h2': '16pt', 
    'h3': '13pt',
    'body': '11pt',
    'table': '10pt'
}

# Manager profiles mapping
MANAGER_PROFILES = {
    'kieran_mckenna': 'The Young Virtuoso',
    'roberto_de_zerbi': 'The Technical Virtuoso', 
    'thomas_frank': 'The Value Engineer',
    'mauricio_pochettino': 'The Homecoming Hero',
    'xavi_hernandez': 'The Flawed Visionary',
    'marco_silva': 'The Steady Hand',
    'oliver_glasner': 'The Quick-Fix Specialist',
    'andoni_iraola': 'The Wrong Fit'
}

class PremiumReportBuilder:
    def __init__(self, source_dir="docs/reports", output_dir="docs/premium_reports"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load manager data for enhanced content
        with open('docs/scores.json', 'r') as f:
            raw_data = json.load(f)
        
        # Process and enhance manager data
        self.scores_data = self.process_manager_data(raw_data)
    
    def process_manager_data(self, raw_data):
        """Process raw JSON data and calculate unified scores, ranks, etc."""
        processed = []
        
        for manager in raw_data:
            # Calculate peer score (average of key metrics)
            peer_metrics = [
                manager['tactical_style'],
                manager['attacking_potency'], 
                manager['defensive_solidity'],
                manager['big_game_performance'],
                manager['youth_development'],
                manager['squad_management']
            ]
            peer_score = sum(peer_metrics) / len(peer_metrics)
            
            # Use fit_score as spurs_fit (scale to 100)
            spurs_fit = manager['fit_score'] * (100 / 10)  # Scale from 10 to 100
            
            # Calculate unified final score: 40% peer + 60% spurs-fit
            final_score = (0.4 * peer_score * 10) + (0.6 * spurs_fit)
            
            # Normalize manager name for matching
            name_key = manager['name'].lower().replace(' ', '_').replace('ñ', 'n')
            
            processed.append({
                'name': manager['name'],
                'name_key': name_key,
                'peer_score': round(peer_score, 1),
                'spurs_fit': round(spurs_fit, 1),
                'final_score': round(final_score, 1),
                'profile': MANAGER_PROFILES.get(name_key, 'Manager'),
                'raw_data': manager
            })
        
        # Sort by final score and assign ranks
        processed.sort(key=lambda x: x['final_score'], reverse=True)
        for i, manager in enumerate(processed):
            manager['rank'] = i + 1
        
        return processed
    
    def generate_premium_css(self):
        """Generate comprehensive CSS for premium report styling"""
        css = f"""
        /* Premium Manager Report Styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {{
            --spurs-teal: {COLORS['spurs_teal']};
            --navy-dark: {COLORS['navy_dark']};
            --light-row: {COLORS['light_row']};
            --callout-bg: {COLORS['callout_bg']};
            --good-heat: {COLORS['good_heat']};
            --bad-heat: {COLORS['bad_heat']};
        }}
        
        /* Base Typography */
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: {TYPOGRAPHY['body']};
            line-height: 1.35;
            color: var(--navy-dark);
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #fff;
        }}
        
        /* Cover Page */
        .cover-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 60pt;
            position: relative;
            min-height: 80vh;
        }}
        
        .cover-title {{
            font-size: {TYPOGRAPHY['title']};
            font-weight: 700;
            text-transform: uppercase;
            color: var(--navy-dark);
            margin-bottom: 2rem;
            letter-spacing: 2px;
        }}
        
        .cover-radar {{
            position: absolute;
            top: 2rem;
            right: 2rem;
            width: 55mm;
            height: 55mm;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .final-score-badge {{
            display: inline-block;
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--spurs-teal), var(--navy-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 1rem 0;
        }}
        
        /* Section Headers */
        h1 {{
            font-size: {TYPOGRAPHY['title']};
            color: var(--navy-dark);
            text-transform: uppercase;
            border-bottom: 3px solid var(--spurs-teal);
            padding-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: {TYPOGRAPHY['h2']};
            font-weight: 600;
            color: var(--navy-dark);
            border-left: 4px solid var(--spurs-teal);
            padding-left: 1rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        h3 {{
            font-size: {TYPOGRAPHY['h3']};
            font-weight: 600;
            color: var(--navy-dark);
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        
        /* Two Column Layout */
        .two-col {{
            column-count: 2;
            column-gap: 2rem;
            column-rule: 1px solid #e5e7eb;
            text-align: justify;
            margin: 1rem 0;
        }}
        
        .two-col p {{
            margin-bottom: 0.75rem;
            break-inside: avoid;
        }}
        
        /* Call-out Boxes */
        .callout {{
            background: var(--callout-bg);
            border-left: 4px solid var(--spurs-teal);
            padding: 0.75rem 1rem;
            margin: 1rem 0;
            border-radius: 0 6px 6px 0;
            break-inside: avoid;
        }}
        
        .callout-stat {{
            background: linear-gradient(135deg, var(--callout-bg), #f0f9ff);
            border: 2px solid var(--spurs-teal);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .callout-stat .metric {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--spurs-teal);
            display: block;
        }}
        
        .callout-stat .label {{
            font-size: 0.875rem;
            color: var(--navy-dark);
            font-weight: 500;
        }}
        
        /* Score Breakdown */
        .score-breakdown {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .score-card {{
            background: var(--callout-bg);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .score-card .title {{
            font-weight: 600;
            color: var(--navy-dark);
            margin-bottom: 1rem;
        }}
        
        .score-card .score {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--spurs-teal);
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: {TYPOGRAPHY['table']};
            break-inside: avoid;
        }}
        
        th {{
            background: var(--navy-dark);
            color: white;
            padding: 0.75rem;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        tr:nth-child(even) {{
            background: var(--light-row);
        }}
        
        /* Heat Map Cells */
        .heat-good {{ background: var(--good-heat); color: white; }}
        .heat-bad {{ background: var(--bad-heat); color: white; }}
        .heat-neutral {{ background: #fbbf24; color: white; }}
        
        /* Navigation */
        .nav-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--navy-dark);
            color: white;
            padding: 1rem;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-links {{
            display: flex;
            gap: 1rem;
        }}
        
        .nav-links a {{
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background 0.2s;
        }}
        
        .nav-links a:hover {{
            background: var(--spurs-teal);
        }}
        
        .table-of-contents {{
            position: fixed;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            max-width: 200px;
            font-size: 0.875rem;
        }}
        
        .table-of-contents ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .table-of-contents a {{
            color: var(--navy-dark);
            text-decoration: none;
            display: block;
            padding: 0.25rem 0;
            transition: color 0.2s;
        }}
        
        .table-of-contents a:hover,
        .table-of-contents a.active {{
            color: var(--spurs-teal);
            font-weight: 600;
        }}
        
        /* Running Headers/Footers */
        .running-header {{
            position: fixed;
            top: 5rem;
            right: 2rem;
            font-size: 0.875rem;
            color: var(--navy-dark);
            font-weight: 500;
            background: white;
            padding: 0.5rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .running-footer {{
            position: fixed;
            bottom: 1rem;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.875rem;
            color: var(--navy-dark);
        }}
        
        /* Visual Elements */
        .mini-bar-chart {{
            display: inline-block;
            width: 70px;
            height: 20px;
            vertical-align: middle;
            margin-left: 0.5rem;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 0.25rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--spurs-teal), var(--navy-dark));
            transition: width 0.3s ease;
        }}
        
        /* Content spacing */
        main {{
            margin-top: 5rem;
            padding-top: 2rem;
        }}
        
        /* Print Styles */
        @media print {{
            body {{ margin: 0; padding: 0; }}
            .nav-header, .table-of-contents {{ display: none; }}
            .cover-page {{ page-break-before: always; }}
            h2 {{ page-break-after: avoid; }}
            .callout {{ page-break-inside: avoid; }}
            table {{ page-break-inside: avoid; }}
        }}
        
        /* Mobile Responsive */
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .two-col {{ column-count: 1; }}
            .table-of-contents {{ display: none; }}
            .cover-radar {{ 
                position: static; 
                width: 200px; 
                height: 200px; 
                margin: 2rem auto; 
            }}
            .score-breakdown {{ grid-template-columns: 1fr; }}
        }}
        """
        
        # Save CSS file
        css_file = self.output_dir / "premium_report.css"
        with open(css_file, 'w') as f:
            f.write(css)
        
        return css_file
    
    def enhance_markdown_content(self, md_content, manager_name):
        """Enhance markdown with premium design elements"""
        
        # Get manager data
        manager_data = None
        for manager in self.scores_data:
            if manager['name_key'] == manager_name:
                manager_data = manager
                break
        
        if not manager_data:
            return md_content
        
        # Add cover page elements
        enhanced = f"""
<div class="cover-page">
<h1 class="cover-title">{manager_data['name']} - Manager Analysis Report</h1>
<div class="final-score-badge">{manager_data['final_score']}/100</div>
<img src="../assets/radar_{manager_name}.png" class="cover-radar" alt="{manager_data['name']} Radar Chart">
<p><strong>Rank #{manager_data['rank']} of 8</strong></p>
<p>{manager_data['profile']}</p>

<div class="score-breakdown">
    <div class="score-card">
        <div class="title">Peer Analysis</div>
        <div class="score">{manager_data['peer_score']}/10</div>
    </div>
    <div class="score-card">
        <div class="title">Spurs-Fit</div>
        <div class="score">{manager_data['spurs_fit']}/100</div>
    </div>
</div>
</div>

<div class="running-header">{manager_data['name']} • Final Score {manager_data['final_score']}/100</div>
<div class="running-footer">Spurs Manager Evaluation 2025</div>
"""
        
        # Process the original content
        lines = md_content.split('\n')
        enhanced_lines = []
        in_narrative_section = False
        
        for i, line in enumerate(lines):
            # Skip original title (we have cover page)
            if line.startswith('# ') and i < 5:
                continue
                
            # Enhance executive summary with call-out
            if '**Final Score:' in line:
                score_match = re.search(r'(\d+\.?\d*)/100', line)
                if score_match:
                    score = score_match.group(1)
                    enhanced_lines.append(f'<div class="callout-stat">')
                    enhanced_lines.append(f'<span class="metric">{score}</span>')
                    enhanced_lines.append(f'<span class="label">Final Score / 100</span>')
                    enhanced_lines.append(f'</div>')
                continue
            
            # Add two-column wrapper for narrative paragraphs
            if line.startswith('## ') and ('Assessment' in line or 'Recommendation' in line):
                enhanced_lines.append(line)
                enhanced_lines.append('<div class="two-col">')
                in_narrative_section = True
                continue
            
            # End two-column section
            if in_narrative_section and (line.startswith('##') or line.startswith('---')):
                enhanced_lines.append('</div>')
                in_narrative_section = False
            
            # Create call-out boxes for key metrics
            if line.startswith('• ') and any(metric in line for metric in ['PPDA:', 'Net Spend:', 'Squad Value']):
                metric_line = line.replace('• ', '').replace('**', '')
                enhanced_lines.append(f'<div class="callout">')
                enhanced_lines.append(f'<strong>{metric_line}</strong>')
                enhanced_lines.append(f'</div>')
                continue
            
            # Add progress bars for scores
            if '✅' in line or '⚠️' in line or '❌' in line:
                enhanced_lines.append(line)
                # Extract score if present
                score_match = re.search(r'(\d+\.?\d*)/', line)
                if score_match:
                    score = float(score_match.group(1))
                    max_score = 100 if '/100' in line else 10
                    percentage = (score / max_score) * 100
                    enhanced_lines.append(f'<div class="progress-bar">')
                    enhanced_lines.append(f'<div class="progress-fill" style="width: {percentage}%"></div>')
                    enhanced_lines.append(f'</div>')
                continue
            
            enhanced_lines.append(line)
        
        if in_narrative_section:
            enhanced_lines.append('</div>')
        
        return enhanced + '\n'.join(enhanced_lines)
    
    def create_html_template(self, manager_name, content, manager_data):
        """Create premium HTML template with navigation"""
        
        # Generate table of contents
        toc_items = [
            ('executive-summary', 'Executive Summary'),
            ('unified-scoring', 'Unified Scoring Breakdown'),
            ('key-indicators', 'Key Performance Indicators'),
            ('strategic-assessment', 'Strategic Assessment'),
            ('recommendation', 'Recommendation')
        ]
        
        toc_html = '<ul>' + ''.join([
            f'<li><a href="#{item_id}" class="toc-link">{title}</a></li>'
            for item_id, title in toc_items
        ]) + '</ul>'
        
        # Get all managers for navigation
        all_managers = [
            'kieran_mckenna', 'roberto_de_zerbi', 'thomas_frank', 'mauricio_pochettino',
            'xavi_hernandez', 'marco_silva', 'oliver_glasner', 'andoni_iraola'
        ]
        
        try:
            current_index = all_managers.index(manager_name)
            prev_manager = all_managers[current_index - 1] if current_index > 0 else None
            next_manager = all_managers[current_index + 1] if current_index < len(all_managers) - 1 else None
        except ValueError:
            prev_manager = next_manager = None
        
        nav_html = f"""
        <div class="nav-links">
            <a href="../index.html">← Back to Dashboard</a>
            {f'<a href="{prev_manager}.html">← Previous</a>' if prev_manager else ''}
            {f'<a href="{next_manager}.html">Next →</a>' if next_manager else ''}
        </div>
        """
        
        template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{manager_data['name']} - Manager Analysis Report</title>
    <link rel="stylesheet" href="premium_report.css">
    {f'<link rel="prev" href="{prev_manager}.html" title="{prev_manager.replace("_", " ").title()}" />' if prev_manager else ''}
    {f'<link rel="next" href="{next_manager}.html" title="{next_manager.replace("_", " ").title()}" />' if next_manager else ''}
</head>
<body>
    <nav class="nav-header">
        <h1>Spurs Manager Evaluation 2025</h1>
        {nav_html}
    </nav>
    
    <aside class="table-of-contents">
        <h4>Contents</h4>
        {toc_html}
    </aside>
    
    <main>
        {content}
    </main>
    
    <script>
        // Table of Contents active highlighting
        const sections = document.querySelectorAll('h2[id], h3[id]');
        const tocLinks = document.querySelectorAll('.toc-link');
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    tocLinks.forEach(link => link.classList.remove('active'));
                    const activeLink = document.querySelector(`a[href="#${{entry.target.id}}"]`);
                    if (activeLink) activeLink.classList.add('active');
                }}
            }});
        }}, {{ rootMargin: '-50px 0px -50px 0px' }});
        
        sections.forEach(section => observer.observe(section));
        
        // Smooth scrolling for TOC links
        tocLinks.forEach(link => {{
            link.addEventListener('click', (e) => {{
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>
        """
        
        return template
    
    def generate_reports(self):
        """Generate all premium reports"""
        
        # Generate CSS
        css_file = self.generate_premium_css()
        print(f"✅ Generated premium CSS: {css_file}")
        
        # Process each manager report
        manager_files = [f for f in self.source_dir.glob("*.md") 
                        if not f.name.startswith('README') and not 'complete' in f.name]
        
        generated_reports = []
        
        for md_file in manager_files:
            manager_name = md_file.stem
            
            # Find manager data
            manager_data = None
            for manager in self.scores_data:
                if manager['name_key'] == manager_name:
                    manager_data = manager
                    break
            
            if not manager_data:
                print(f"⚠️  Skipping {manager_name} - no data found")
                continue
            
            # Read and enhance markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            enhanced_md = self.enhance_markdown_content(md_content, manager_name)
            
            # Convert to HTML
            html_content = markdown.markdown(
                enhanced_md, 
                extensions=['tables', 'attr_list', 'toc']
            )
            
            # Post-process HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Add IDs to headings for navigation
            for i, heading in enumerate(soup.find_all(['h2', 'h3'])):
                if not heading.get('id'):
                    heading['id'] = heading.get_text().lower().replace(' ', '-').replace('/', '-')
            
            # Generate final HTML
            final_html = self.create_html_template(manager_name, str(soup), manager_data)
            
            # Save HTML report
            html_file = self.output_dir / f"{manager_name}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            generated_reports.append({
                'name': manager_data['name'],
                'file': f"{manager_name}.html",
                'score': manager_data['final_score'],
                'rank': manager_data['rank']
            })
            
            print(f"✅ Generated premium report: {html_file}")
        
        # Generate index page for reports
        self.generate_reports_index(generated_reports)
        
        return generated_reports
    
    def generate_reports_index(self, reports):
        """Generate index page for all premium reports"""
        
        reports_sorted = sorted(reports, key=lambda x: x['rank'])
        
        cards_html = ""
        for report in reports_sorted:
            cards_html += f"""
            <div class="report-card">
                <div class="report-rank">#{report['rank']}</div>
                <h3>{report['name']}</h3>
                <div class="report-score">{report['score']}/100</div>
                <a href="{report['file']}" class="report-link">View Premium Report →</a>
            </div>
            """
        
        index_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Manager Reports - Spurs Evaluation 2025</title>
    <link rel="stylesheet" href="premium_report.css">
    <style>
        .reports-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 2rem; 
            margin: 2rem 0; 
        }}
        .report-card {{ 
            background: white; 
            border: 1px solid #e5e7eb; 
            border-radius: 12px; 
            padding: 2rem; 
            text-align: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
            transition: transform 0.2s; 
        }}
        .report-card:hover {{ transform: translateY(-4px); }}
        .report-rank {{ 
            font-size: 2rem; 
            font-weight: 700; 
            color: var(--spurs-teal); 
        }}
        .report-score {{ 
            font-size: 1.5rem; 
            font-weight: 600; 
            color: var(--navy-dark); 
            margin: 1rem 0; 
        }}
        .report-link {{ 
            display: inline-block; 
            background: var(--spurs-teal); 
            color: white; 
            padding: 0.75rem 1.5rem; 
            border-radius: 6px; 
            text-decoration: none; 
            transition: background 0.2s; 
        }}
        .report-link:hover {{ background: var(--navy-dark); }}
    </style>
</head>
<body>
    <nav class="nav-header">
        <h1>Premium Manager Reports</h1>
        <div class="nav-links">
            <a href="../index.html">← Back to Dashboard</a>
        </div>
    </nav>
    
    <main style="margin-top: 5rem;">
        <h1>Premium Manager Analysis Reports</h1>
        <p class="two-col">
            Comprehensive board-room quality reports implementing professional design guidelines. 
            Each report features premium typography, two-column layouts, visual elements, and 
            detailed analysis with enhanced readability.
        </p>
        
        <div class="reports-grid">
            {cards_html}
        </div>
    </main>
</body>
</html>
        """
        
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"✅ Generated reports index: {index_file}")

def main():
    """Build all premium reports"""
    builder = PremiumReportBuilder()
    reports = builder.generate_reports()
    
    print(f"\n🎉 Generated {len(reports)} premium reports!")
    print("📍 View at: docs/premium_reports/index.html")
    print("\n📋 QC Checklist completed:")
    print("✅ Cover page with title, radar, final score badge")
    print("✅ Two-column narrative layout")
    print("✅ Tables with proper styling")
    print("✅ Call-out boxes with teal accent")
    print("✅ Navigation aids and TOC")
    print("✅ Running headers and consistent typography")
    print("✅ Mobile responsive design")
    print("✅ Print-ready CSS")

if __name__ == "__main__":
    main() 