import threading
import queue
import json
import os
import re
from collections import Counter

# --- Thread-Safe Globals ---
visited_urls = set()
index_data = [] # Stores dicts: {url, origin, depth, title, text}
url_queue = queue.Queue(maxsize=1000) # Maxsize creates native backpressure
lock = threading.Lock()
is_indexing = False

STATE_FILE = "state.json"


def export_p_data():
    try:
        print("[System] preparing files for p.data...")
        os.makedirs(os.path.join('data', 'storage'), exist_ok=True)
        
        file_path = os.path.join('data', 'storage', 'p.data')
        print(f"[System] Writing data on this file: {file_path}")
        
        yazilan_satir = 0
        with lock:
            with open(file_path, 'w', encoding='utf-8') as f:
                for page in index_data:
                    text = page['title'] + " " + page['text']
                    words = re.findall(r'\w+', text.lower())
                    freqs = Counter(words)
                    
                    for word, freq in freqs.items():
                        f.write(f"{word} {page['url']} {page['origin']} {page['depth']} {freq}\n")
                        yazilan_satir += 1
                        
        print(f"[System] SUCCESS! p.data is created. Total {yazilan_satir} words are saved.")
        print(f"[System] File path: {os.path.abspath(file_path)}")
    except Exception as e:
        print(f"[SYSTEM ERROR] there is an error while creating p.data: {e}")

def save_state():
    print("[System] Saving state...")
    with lock:
        state = {
            'visited': list(visited_urls),
            'index': index_data,
        }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)
    
    # p.data'yı dışarı aktar
    export_p_data()

def load_state():
    global visited_urls, index_data
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            visited_urls = set(state.get('visited', []))
            index_data = state.get('index', [])
        print(f"[System] Resumed from state. Loaded {len(visited_urls)} visited URLs.")

