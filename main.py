import state
from crawler import index
from search import search_query
from server import run_api_server
import threading

def start_cli():
    state.load_state()
    print("\n--- Localhost Crawler & Search Engine ---")
    print("Commands: 'index <url> <depth>', 'search <query>', 'status', 'exit'")
    
    while True:
        try:
            cmd_input = input("\n> ").strip().split(" ", 1)
            if not cmd_input[0]: continue
            cmd = cmd_input[0].lower()
            args = cmd_input[1] if len(cmd_input) > 1 else ""

            if cmd == "index":
                parts = args.split()
                if len(parts) == 2:
                    index(parts[0], parts[1])
                else:
                    print("Usage: index <url> <depth>")
                    
            elif cmd == "search":
                if args:
                    res = search_query(args)
                    print(f"\nFound {len(res)} results:")
                    for r in res:
                        print(f" - URL: {r[0]} | Origin: {r[1]} | Depth: {r[2]}")
                else:
                    print("Usage: search <query>")
                    
            elif cmd == "status":
                q_size = state.url_queue.qsize()
                bp_status = "Active (Throttling)" if q_size >= state.url_queue.maxsize else "Inactive (Healthy)"
                print("\n--- System Status ---")
                print(f"Indexed Pages:  {len(state.index_data)}")
                print(f"Visited URLs:   {len(state.visited_urls)}")
                print(f"Queue Depth:    {q_size} / {state.url_queue.maxsize}")
                print(f"Backpressure:   {bp_status}")
                
            elif cmd == "exit":
                print("Saving state and exiting...")
                state.save_state()
                break
            elif cmd == "serve":
                print("Starting API Server on port 3600...")
                server_thread = threading.Thread(target=run_api_server)
                server_thread.daemon = True
                server_thread.start()
            else:
                print("Unknown command.")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_cli()