import psutil
import sys

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.kill()
        print(f"Process {pid} killed successfully.")
    except psutil.NoSuchProcess:
        print(f"Process {pid} not found.")
    except psutil.AccessDenied:
        print(f"Permission denied. Cannot kill process {pid}.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_killer.py <PID>")
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
        kill_process(pid)
    except ValueError:
        print("Invalid PID. Please enter a numeric process ID.")
