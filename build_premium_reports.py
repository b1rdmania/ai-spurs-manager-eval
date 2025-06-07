#!/usr/bin/env python3
"""
Premium Manager Report Builder - Simplified Version
Uses correct unified final scores data
"""

import os
import pandas as pd
import markdown
from bs4 import BeautifulSoup
from pathlib import Path

# Manager profiles mapping
MANAGER_PROFILES = {
    'Kieran McKenna': 'The Young Virtuoso',
    'Roberto De Zerbi': 'The Technical Virtuoso', 
    'Thomas Frank': 'The Value Engineer',
    'Mauricio Pochettino': 'The Homecoming Hero',
    'Xavi Hernández': 'The Flawed Visionary',
    'Marco Silva': 'The Steady Hand',
    'Oliver Glasner': 'The Quick-Fix Specialist',
    'Andoni Iraola': 'The Wrong Fit'
}

class PremiumReportBuilder:
    def __init__(self, source_dir="docs/reports", output_dir="docs/premium_reports"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load correct unified scores data
        self.scores_data = self.load_unified_scores()
    
    def load_unified_scores(self):
        """Load the correct unified final scores from CSV"""
        scores_file = 'deliverables/data/scores_unified.csv'
        if not os.path.exists(scores_file):
            print(f"❌ Scores file not found: {scores_file}")
            return []
        
        df = pd.read_csv(scores_file)
        
        processed = []
        for _, row in df.iterrows():
            processed.append({
                'name': row['manager_name'],
                'final_score': round(row['final_score'], 1),
                'peer_score': round(row['peer_score'], 1), 
                'spursfit_total': round(row['spursfit_total'], 1),
                'rank': int(row['rank']),
                'profile': MANAGER_PROFILES.get(row['manager_name'], 'Manager')
            })
        
        return processed
    
    def generate_simple_css(self):
        """Generate simple, clean CSS"""
        css = """
        /* Simple Premium Report Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: #fff;
        }
        
        h1 {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #132257;
            border-bottom: 2px solid #50e3c2;
            padding-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            color: #132257;
        }
        
        h3 {
            font-size: 1.2rem;
            font-weight: 500;
            margin: 1.5rem 0 0.5rem 0;
            color: #132257;
        }
        
        p {
            margin-bottom: 1rem;
        }
        
        .cover-header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #132257, #50e3c2);
            color: white;
            border-radius: 8px;
        }
        
        .final-score {
            font-size: 3rem;
            font-weight: 700;
            margin: 1rem 0;
        }
        
        .rank-badge {
            background: #50e3c2;
            color: #132257;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .score-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .score-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #50e3c2;
        }
        
        .score-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #132257;
        }
        
        ul {
            margin: 1rem 0;
            padding-left: 2rem;
        }
        
        li {
            margin-bottom: 0.5rem;
        }
        
        .nav-header {
            background: #132257;
            color: white;
            padding: 1rem;
            margin: -2rem -2rem 2rem -2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .nav-header a {
            color: #50e3c2;
            text-decoration: none;
            font-weight: 500;
        }
        
        .nav-header a:hover {
            text-decoration: underline;
        }
        
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1rem 0;
        }
        """
        
        css_file = self.output_dir / 'premium_report.css'
        with open(css_file, 'w') as f:
            f.write(css)
        print(f"✅ Generated simple CSS: {css_file}")
    
    def get_manager_data(self, manager_name):
        """Get data for a specific manager"""
        for manager in self.scores_data:
            if manager['name'] == manager_name:
                return manager
        return None
    
    def process_markdown_file(self, md_file):
        """Process a single markdown file"""
        # Skip duplicate files and README
        filename = md_file.name.lower()
        if 'complete' in filename or 'readme' in filename:
            return None
            
        # Extract and normalize manager name from filename
        manager_name_raw = md_file.stem.replace('_', ' ')
        
        # Handle special case mappings
        name_mappings = {
            'kieran mckenna': 'Kieran McKenna',
            'roberto de zerbi': 'Roberto De Zerbi',
            'thomas frank': 'Thomas Frank',
            'mauricio pochettino': 'Mauricio Pochettino',
            'xavi hernandez': 'Xavi Hernández',
            'xavi hernández': 'Xavi Hernández',
            'marco silva': 'Marco Silva',
            'oliver glasner': 'Oliver Glasner',
            'andoni iraola': 'Andoni Iraola'
        }
        
        manager_name = name_mappings.get(manager_name_raw.lower(), manager_name_raw.title())
        
        # Get unified scores data
        manager_data = self.get_manager_data(manager_name)
        if not manager_data:
            print(f"⚠️ No data found for: {manager_name}")
            return None
        
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert to HTML
        md = markdown.Markdown()
        html_content = md.convert(content)
        
        # Create simple HTML template
        html = self.create_simple_html(manager_name, html_content, manager_data)
        
        # Save HTML file
        output_file = self.output_dir / f"{md_file.stem}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated: {output_file}")
        return output_file
    
    def create_simple_html(self, manager_name, content, manager_data):
        """Create simplified HTML template"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{manager_name} - Manager Analysis Report</title>
    <link rel="stylesheet" href="premium_report.css">
</head>
<body>
    <nav class="nav-header">
        <h1>Spurs Manager Evaluation 2025</h1>
        <div>
            <a href="../index.html">← Back to Dashboard</a>
        </div>
    </nav>
    
    <div class="cover-header">
        <h1>{manager_name}</h1>
        <div class="rank-badge">Rank #{manager_data['rank']} of 8</div>
        <div class="final-score">{manager_data['final_score']}/100</div>
        <p><strong>{manager_data['profile']}</strong></p>
        
        <div class="score-grid">
            <div class="score-card">
                <div>Peer Analysis</div>
                <div class="score-value">{manager_data['peer_score']}/10</div>
            </div>
            <div class="score-card">
                <div>Spurs-Fit</div>
                <div class="score-value">{manager_data['spursfit_total']}/100</div>
            </div>
        </div>
    </div>
    
    {content}
    
</body>
</html>"""
        return html
    
    def generate_reports(self):
        """Generate all premium reports"""
        # Generate CSS
        self.generate_simple_css()
        
        # Process each markdown file
        reports = []
        for md_file in self.source_dir.glob("*.md"):
            output_file = self.process_markdown_file(md_file)
            if output_file:
                reports.append(output_file)
        
        # Generate index page
        self.generate_simple_index(reports)
        
        print(f"\n🎉 Generated {len(reports)} premium reports in {self.output_dir}")
        return reports
    
    def generate_simple_index(self, reports):
        """Generate simple index page"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Manager Reports</title>
    <link rel="stylesheet" href="premium_report.css">
</head>
<body>
    <nav class="nav-header">
        <h1>Premium Manager Reports</h1>
        <div>
            <a href="../index.html">← Back to Dashboard</a>
        </div>
    </nav>
    
    <h1>Premium Manager Reports</h1>
    <p>Detailed analysis of all 8 manager candidates using our Unified Final Scoring System.</p>
    
    <h2>Manager Reports</h2>
    <div style="display: grid; gap: 1rem; margin-top: 2rem;">
"""
        
        # Add manager links sorted by rank
        sorted_managers = sorted(self.scores_data, key=lambda x: x['rank'])
        for manager in sorted_managers:
            filename = manager['name'].lower().replace(' ', '_').replace('ñ', 'n') + '.html'
            html += f"""
        <div class="score-card" style="text-align: left;">
            <h3>#{manager['rank']}. <a href="{filename}">{manager['name']}</a></h3>
            <p><strong>{manager['final_score']}/100</strong> • {manager['profile']}</p>
            <p>Peer: {manager['peer_score']}/10 • Spurs-Fit: {manager['spursfit_total']}/100</p>
        </div>"""
        
        html += """
    </div>
</body>
</html>"""
        
        index_file = self.output_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated index: {index_file}")

def main():
    builder = PremiumReportBuilder()
    builder.generate_reports()

if __name__ == "__main__":
    main() 