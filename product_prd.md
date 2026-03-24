# Product Requirements Document: Localhost Web Crawler

## 1. Objective
Build a concurrent web crawler and real-time search engine using strictly language-native functionality to demonstrate architectural sensibility, thread-safety, and backpressure management.

## 2. Core Constraints
*   **Language-Native:** Must use Python's built-in libraries (`urllib`, `html.parser`, `threading`, `queue`). High-level libraries (Scrapy, BeautifulSoup, Requests) are strictly prohibited.
*   **Concurrency:** Search must be fully functional and non-blocking while the Indexer is actively crawling.

## 3. Capabilities

### 3.1 Indexer (`/index`)
*   **Inputs:** `origin` (URL string), `k` (maximum depth integer).
*   **Behavior:** Initiates a recursive crawl up to depth `k`. Uses a "Visited" set protected by a Mutex/Lock to guarantee uniqueness.
*   **Backpressure:** Uses a bounded queue (`queue.Queue(maxsize)`) to manage load. If the queue is full, worker threads block on `put()`, naturally throttling network extraction.

### 3.2 Searcher (`/search`)
*   **Inputs:** `query` (string).
*   **Outputs:** A list of triples: `(relevant_url, origin_url, depth)`.
*   **Relevancy Heuristic:** Ranks results based on Term Frequency (TF). Keywords found in the `<title>` are weighted 5x heavier than keywords found in the body text.

### 3.3 Visibility & Resumability
*   **Dashboard:** A CLI interface displaying Indexing Progress, Queue Depth, and Backpressure status.
*   **Persistence:** State (visited set and index datastore) is periodically flushed to a local `state.json` file to allow resumability upon interruption.