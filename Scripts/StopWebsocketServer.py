# kill_server.py
import os
import signal

# Function to kill the server based on the saved pid
def kill_server():
    try:
        # Read the process id from the file
        with open("server_pid.txt", "r") as f:
            pid = int(f.read().strip())
        
        # Send SIGTERM to the process
        os.kill(pid, signal.SIGTERM)
        print(f"WebSocket server with PID {pid} terminated.")
        
        # Optionally remove the PID file
        os.remove("server_pid.txt")
    except FileNotFoundError:
        print("PID file not found. Is the server running?")
    except ProcessLookupError:
        print("No such process is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    kill_server()