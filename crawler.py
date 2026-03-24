import threading
import queue
import state
from parser_utils import fetch_and_parse

def worker():
    while True:
        try:
            current_url, origin, depth, max_depth = state.url_queue.get(timeout=2)
            
            with state.lock:
                if current_url in state.visited_urls:
                    state.url_queue.task_done()
                    continue
                state.visited_urls.add(current_url)

            # Fetch
            links, title, text = fetch_and_parse(current_url)
            
            # Index
            with state.lock:
                if title or text:
                    state.index_data.append({
                        'url': current_url,
                        'origin': origin,
                        'depth': depth,
                        'title': title,
                        'text': text
                    })

            # Queue new links if under max depth
            if depth < max_depth:
                for link in links:
                    with state.lock:
                        if link not in state.visited_urls:
                            state.url_queue.put((link, origin, depth + 1, max_depth))
            
            state.url_queue.task_done()
            state.save_state()
            
        except queue.Empty:
            if not state.is_indexing:
                break

def index(origin, k):
    state.is_indexing = True
    state.url_queue.put((origin, origin, 0, int(k)))
    
    for _ in range(5):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    print(f"[*] Indexing initiated for {origin} up to depth {k}.")