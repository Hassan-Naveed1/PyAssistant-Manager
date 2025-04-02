from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from pyassistant.models import Host
import paramiko
import logging

def get_process_data_from_remote(host_ip, username, password):
    # First, I am setting up an SSH client to connect to the remote machine.
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Now, I will connect to the remote machine using SSH credentials.
        client.connect(host_ip, username=username, password=password)
        
        # Once connected, I will run the `ps -eo pid,ppid,pcpu,pmem,etime,comm` command to get process info with parent-child relation.
        stdin, stdout, stderr = client.exec_command("ps -eo pid,ppid,pcpu,pmem,etime,comm")

        process_list = []
        # Now, I will read the output, split it into lines, and extract process details.
        for line in stdout.read().decode().splitlines()[1:]:  
            columns = line.split(None, 5)
            if len(columns) == 6:
                process_list.append({
                    'pid': int(columns[0]),         # Extracting Process ID
                    'ppid': int(columns[1]),        # Extracting Parent Process ID
                    'cpu_usage': float(columns[2]), # CPU Usage
                    'memory_usage': float(columns[3]), # Memory Usage
                    'execution_time': columns[4],   # Execution Time
                    'name': columns[5]              # Extracting Process Name
                })

        # I will collect all parent PIDs from the list to determine which processes have children.
        all_ppids = {proc['ppid'] for proc in process_list}

        # Now, I will mark each process with has_children=True if its PID is found in the list of PPIDs.
        for proc in process_list:
            proc['has_children'] = proc['pid'] in all_ppids

        return process_list

    except Exception as e:
        # If something goes wrong, I will log the error and return an error message.
        logging.error(f"SSH Error: {e}")
        return {"error": f"SSH Connection Failed: {str(e)}"}

    finally:
        # I will close the SSH connection after the data is retrieved.
        client.close()

def host_processes_view(request, host_id):
    # First, I will get the host details using the host ID.
    host = get_object_or_404(Host, id=host_id)  

    # Now, I will fetch all the running processes from that host via SSH.
    processes = get_process_data_from_remote(host.ip_address, host.username, host.password)

    # Finally, I will render the `host_processes.html` template with the host and processes data.
    return render(request, 'monitor/host_processes.html', {
        'host': host,
        'processes': processes
    })


def kill_process_view(request, host_id, pid):
    # First, I will check if the request method is `POST`. If not, I will return an error.
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

    # Now, I will get the host details based on the provided `host_id`.
    host = get_object_or_404(Host, id=host_id)

    try:
        # I will set up an SSH connection to the remote host.
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host.ip_address, username=host.username, password=host.password)

        # Now, I will check whether the remote machine is running Linux or Windows.
        stdin, stdout, stderr = client.exec_command("uname")
        os_type = stdout.read().decode().strip()

        if os_type == "Linux":
            # If it is Linux, I will use the `kill -9` command to terminate the process.
            kill_command = f"kill -9 {pid}"
        else:
            # If it is Windows, I will use `taskkill` to terminate the process.
            kill_command = f"taskkill /F /PID {pid}"

        # Now, I will execute the kill command on the remote machine.
        stdin, stdout, stderr = client.exec_command(kill_command)
        error = stderr.read().decode().strip()

        # After executing the command, I will close the SSH connection.
        client.close()

        # If there was an error, I will return the error message.
        if error:
            return JsonResponse({"success": False, "message": f"Error: {error}"})
        
        # Otherwise, I will return a success message.
        return JsonResponse({"success": True, "message": f"Process {pid} killed successfully on {host.hostname}."})

    except Exception as e:
        # If anything goes wrong, I will log the error and return an error message.
        logging.error(f"Kill process error: {e}")
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)
