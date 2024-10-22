import os
import signal

# Function to kill the server
def kill_server():
    try:
        # Read the PID from the file
        with open("server_pid.txt", "r") as pid_file:
            pid = int(pid_file.read().strip())

        # Kill the process using the stored PID
        os.kill(pid, signal.SIGTERM)

        print(f"Server with PID {pid} has been terminated.")
        # Optionally, remove the PID file
        os.remove("server_pid.txt")
    except FileNotFoundError:
        print("No server PID file found. Is the server running?")
    except ProcessLookupError:
        print("No process found with the stored PID.")
    except Exception as e:
        print(f"Error killing server: {e}")

if __name__ == "__main__":
    kill_server()