"""
Simple HTTP server to serve the frontend pages.
Run this from the frontend directory to serve the UI.
"""
import http.server
import socketserver
import os
import sys

PORT = 3000
DIRECTORY = "public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("DICT PROCUREMENT MANAGEMENT SYSTEM - Frontend Server")
        print("=" * 60)
        print("")
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Serving files from: {DIRECTORY}/")
        print("")
        print("AVAILABLE PAGES:")
        print(f"  - Master Index: http://localhost:{PORT}/index.html")
        print(f"  - Login Page:   http://localhost:{PORT}/login.html")
        print(f"  - Dashboard:    http://localhost:{PORT}/dashboard.html")
        print(f"  - Users:        http://localhost:{PORT}/users.html")
        print(f"  - PR List:      http://localhost:{PORT}/purchase-requests.html")
        print(f"  - Create PR:    http://localhost:{PORT}/create-pr.html")
        print("")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print("")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("")
            print("=" * 60)
            print("Server stopped.")
            print("=" * 60)
            sys.exit(0)
