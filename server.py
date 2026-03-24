import http.server
import socketserver
import urllib.parse
import json
import re
import state

class SearchAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Sadece /search endpoint'ini dinle
        if parsed_path.path == '/search':
            query_params = urllib.parse.parse_qs(parsed_path.query)
            query = query_params.get('query', [''])[0].lower()
            
            results = []
            with state.lock:
                for page in state.index_data:
                    text = page['title'] + " " + page['text']
                    words = re.findall(r'\w+', text.lower())
                    freq = words.count(query)
                    
                    if freq > 0:
                        depth = page['depth']
                        # HOCANIN VERDİĞİ FORMÜL: score = (frequency x 10) + 1000 - (depth x 5)
                        score = (freq * 10) + 1000 - (depth * 5)
                        
                        results.append({
                            'url': page['url'],
                            'relevance_score': score,
                            'origin': page['origin'],
                            'depth': depth,
                            'frequency': freq
                        })
            
            # Puanı en yüksek olanı en başa al
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Sonuçları JSON olarak gönder
            self.wfile.write(json.dumps(results).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_api_server():
    PORT = 3600
    handler = SearchAPIHandler
    # Adres zaten kullanımdaysa hata vermemesi için ayar
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\n[+] API Server is working! You can test here: http://localhost:{PORT}/search?query=world")
        httpd.serve_forever()