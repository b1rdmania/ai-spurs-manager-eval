#!/usr/bin/env python3
"""
Simple local server to preview the generated website
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def serve_site():
    """Start a local web server to preview the site"""
    
    # Change to docs directory
    docs_path = Path('deliverables/docs')
    if not docs_path.exists():
        print("❌ Docs folder not found. Run generate_frozen_package.py first!")
        return
    
    os.chdir(docs_path)
    
    # Start server
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Serving website at http://localhost:{PORT}")
        print("📊 Preview the manager evaluation dashboard")
        print("🔗 Press Ctrl+C to stop")
        
        # Try to open browser
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
            
        httpd.serve_forever()

if __name__ == "__main__":
    serve_site() 