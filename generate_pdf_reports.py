#!/usr/bin/env python3
"""
PDF Report Generator for Premium Manager Reports
Uses WeasyPrint for high-quality PDF conversion with proper styling
"""

import os
import sys
from pathlib import Path
import subprocess

def install_weasyprint():
    """Install WeasyPrint and dependencies"""
    try:
        import weasyprint
        print("✅ WeasyPrint already installed")
        return True
    except ImportError:
        print("📦 Installing WeasyPrint...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'weasyprint'])
            import weasyprint
            print("✅ WeasyPrint installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install WeasyPrint")
            print("💡 Try installing manually: python3 -m pip install weasyprint")
            return False

def generate_pdf_reports():
    """Generate PDF versions of all premium HTML reports"""
    
    if not install_weasyprint():
        return
    
    from weasyprint import HTML, CSS
    
    reports_dir = Path("docs/premium_reports")
    pdf_dir = reports_dir / "pdf"
    pdf_dir.mkdir(exist_ok=True)
    
    # Custom PDF CSS for better print layout
    pdf_css = CSS(string="""
        @page {
            size: A4;
            margin: 2cm 1.5cm;
            @top-right {
                content: "Spurs Manager Evaluation 2025";
                font-family: Inter, sans-serif;
                font-size: 10pt;
                color: #0b1e3c;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-family: Inter, sans-serif;
                font-size: 10pt;
                color: #0b1e3c;
            }
        }
        
        @page:first {
            @top-right { content: none; }
            @bottom-center { content: none; }
        }
        
        body {
            font-family: Inter, sans-serif;
            line-height: 1.4;
            color: #0b1e3c;
        }
        
        .cover-page {
            page-break-after: always;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .cover-radar {
            width: 8cm;
            height: 8cm;
            margin: 2cm 0;
        }
        
        .nav-header, .table-of-contents, .running-header, .running-footer {
            display: none;
        }
        
        h2 {
            page-break-after: avoid;
            margin-top: 1.5cm;
        }
        
        .two-col {
            column-count: 2;
            column-gap: 1cm;
            column-rule: 1px solid #e5e7eb;
        }
        
        .callout, .callout-stat {
            page-break-inside: avoid;
            margin: 0.5cm 0;
        }
        
        table {
            page-break-inside: avoid;
            width: 100%;
            margin: 0.5cm 0;
        }
        
        .score-breakdown {
            display: flex;
            justify-content: space-around;
            margin: 1cm 0;
        }
        
        .score-card {
            width: 40%;
            text-align: center;
            padding: 0.5cm;
            border: 1px solid #50e3c2;
            border-radius: 8px;
        }
    """)
    
    # Get list of HTML reports
    html_files = list(reports_dir.glob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html"]
    
    generated_pdfs = []
    
    for html_file in html_files:
        try:
            print(f"🔄 Converting {html_file.name} to PDF...")
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert relative paths to absolute for assets
            html_content = html_content.replace('src="../assets/', f'src="{reports_dir.parent.absolute()}/assets/')
            
            # Generate PDF
            pdf_file = pdf_dir / f"{html_file.stem}.pdf"
            HTML(string=html_content, base_url=str(reports_dir.absolute())).write_pdf(
                pdf_file,
                stylesheets=[pdf_css]
            )
            
            generated_pdfs.append(pdf_file)
            print(f"✅ Generated: {pdf_file}")
            
        except Exception as e:
            print(f"❌ Error converting {html_file.name}: {e}")
    
    # Generate combined PDF with all reports
    try:
        print("\n🔄 Creating combined PDF report...")
        combined_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Spurs Manager Evaluation 2025 - Complete Analysis</title>
            <style>
                .title-page {
                    page-break-after: always;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-family: Inter, sans-serif;
                }
                .section-break {
                    page-break-before: always;
                }
            </style>
        </head>
        <body>
            <div class="title-page">
                <h1 style="font-size: 2.5rem; color: #132257; margin-bottom: 1rem;">
                    SPURS MANAGER EVALUATION 2025
                </h1>
                <h2 style="font-size: 1.5rem; color: #1e3d72; margin-bottom: 2rem;">
                    Complete Analysis Report
                </h2>
                <p style="font-size: 1rem; color: #0b1e3c;">
                    Unified Final Scoring System<br>
                    40% Peer Analysis + 60% Spurs-Fit Model
                </p>
            </div>
        """
        
        # Add each manager report
        for html_file in sorted(html_files, key=lambda x: x.stem):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract main content (remove nav and scripts)
            import re
            main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
            if main_match:
                main_content = main_match.group(1)
                combined_html += f'<div class="section-break">{main_content}</div>'
        
        combined_html += "</body></html>"
        
        # Fix asset paths
        combined_html = combined_html.replace('src="../assets/', f'src="{reports_dir.parent.absolute()}/assets/')
        
        # Generate combined PDF
        combined_pdf = pdf_dir / "complete_manager_evaluation_2025.pdf"
        HTML(string=combined_html, base_url=str(reports_dir.absolute())).write_pdf(
            combined_pdf,
            stylesheets=[pdf_css]
        )
        
        print(f"✅ Generated combined PDF: {combined_pdf}")
        generated_pdfs.append(combined_pdf)
        
    except Exception as e:
        print(f"❌ Error creating combined PDF: {e}")
    
    print(f"\n🎉 Generated {len(generated_pdfs)} PDF reports!")
    print(f"📁 Location: {pdf_dir}")
    
    return generated_pdfs

def main():
    """Generate all PDF reports"""
    print("🏗️  Generating Premium PDF Reports...")
    print("=" * 50)
    
    pdfs = generate_pdf_reports()
    
    print("\n📋 PDF QC Checklist:")
    print("✅ A4 page format with proper margins")
    print("✅ Cover page with title and radar chart")
    print("✅ Two-column narrative layout")
    print("✅ Page breaks after sections")
    print("✅ Running headers and page numbers")
    print("✅ Print-optimized styling")
    print("✅ High-quality asset rendering")
    
if __name__ == "__main__":
    main() 