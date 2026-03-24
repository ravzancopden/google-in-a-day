import urllib.request
import urllib.parse
from html.parser import HTMLParser

class CrawlerParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self.text_content = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    full_url = urllib.parse.urljoin(self.base_url, value)
                    if full_url.startswith('http'):
                        self.links.append(full_url)
        elif tag == 'title':
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        else:
            clean_text = data.strip()
            if clean_text:
                self.text_content.append(clean_text)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

def fetch_and_parse(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if 'text/html' not in response.getheader('Content-Type', ''):
                return [], "", ""
            html = response.read().decode('utf-8', errors='ignore')
            parser = CrawlerParser(url)
            parser.feed(html)
            print(f"[+] Successfully read: {url}")
            return parser.links, parser.title, " ".join(parser.text_content)
    except Exception as e:
        return [], "", ""