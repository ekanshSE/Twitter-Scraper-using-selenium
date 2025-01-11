from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from scraper import scrape_twitter

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Logging the request path
        print(f"Request received: {self.path}")
        
        if self.path == '/scrape':
            # Set up the response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            try:
                # Call the scraper to fetch trends
                trends = scrape_twitter()
                response = {"success": True, "trends": trends}
                print(f"Trends fetched: {trends}")  # Log the trends for debugging
            except Exception as e:
                print(f"Error occurred: {e}")
                response = {"success": False, "message": str(e)}

            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Server started at http://localhost:8000")
    server.serve_forever()
