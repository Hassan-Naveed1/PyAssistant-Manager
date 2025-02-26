import psutil
import sys
import paramiko
from django.http import JsonResponse
def kill_process(request, pid):
    if request.method == "POST":
        # SSH credentials for the remote machine
        host = '172.20.10.1'  # Replace with the IP or hostname of the remote machine
        username = 'hassan'     # Replace with the SSH username
        password = '123'     # Replace with the SSH password

        try:
            # Establish SSH connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=username, password=password)

            # Kill the process on the remote machine
            kill_command = f"kill {pid}"
            stdin, stdout, stderr = client.exec_command(kill_command)

            # Check for any errors
            error = stderr.read().decode()
            if error:
                return JsonResponse({"success": False, "message": f"Failed to kill process {pid}. Error: {error}"}, status=400)

            # If no error, the process was killed
            client.close()
            return JsonResponse({"success": True, "message": f"Process {pid} termination requested."})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
