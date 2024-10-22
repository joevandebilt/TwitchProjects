import os
import subprocess
import signal

# Function to start the server
def start_server():
    try:
        # Start the server in a new process
        process = subprocess.Popen(['python', '-m', 'http.server', '8000', '--directory', r'D:/My Documents/My Videos/Projects/Twitch/HTML/Quiz'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Save the process ID (PID) to a file so we can kill it later
        with open("server_pid.txt", "w") as pid_file:
            pid_file.write(str(process.pid))

        print(f"Server started with PID {process.pid}. You can access it at http://localhost:8000")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_server()