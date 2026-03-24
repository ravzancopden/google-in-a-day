# Localhost Web Crawler & Search Engine

A high-performance, concurrent web crawler and real-time search engine built entirely from scratch using Python's native standard library. Designed to demonstrate robust system architecture, concurrency management, and "Human-in-the-Loop" AI coding.

## Key Architectural Decisions
*   **Native Tooling:** Built exclusively with `urllib`, `html.parser`, and `threading`. No external dependencies are required.
*   **Thread-Safe Concurrency:** Allows real-time searching via a CLI dashboard while background threads actively crawl and index new pages. Data corruption is prevented using `threading.Lock`.
*   **Native Backpressure:** Utilizes bounded queues (`queue.Queue`). When memory constraints are reached, threads gracefully block, naturally throttling the crawl rate.
*   **Resumability:** Automatically saves the inverted index and visited graph to `state.json` on disk, allowing the crawl to survive unexpected interruptions.

## How to Run
1. Ensure you have Python 3.8+ installed.
2. Clone this repository and navigate to the folder.
3. Run the application:
   ```bash
   python main.py