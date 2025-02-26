from django.shortcuts import render
from django.http import JsonResponse
from pyassistant.models import Host  
import psutil
import datetime
import paramiko
import logging


def get_process_data_from_remote(host_ip, hostname, password):
    """Retrieve process data from a remote host via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        
        client.connect(host_ip, username=hostname, password=password)  
        stdin, stdout, stderr = client.exec_command("ps aux")

        process_list = []
        for line in stdout.read().decode().splitlines()[1:]:  
            columns = line.split()
            if len(columns) > 10:
                process_list.append({
                    'pid': int(columns[1]),
                    'name': columns[10],
                    'cpu_usage': float(columns[2]),
                    'memory_usage': float(columns[3]),
                    'execution_time': columns[9]
                })

        return process_list

    except Exception as e:
        logging.error(f"SSH Error: {e}")
        return []

    finally:
        client.close()


def process_list_view(request):
    """View to fetch remote process data for all hosts in the database."""
    hosts = Host.objects.all()  
    all_processes = {}


    for host in hosts:
        try:
            processes = get_process_data_from_remote(host.ip_address, host.hostname, host.password)
            all_processes[host.hostname] = processes
        except Exception as e:

            all_processes[host.hostname] = f"Error fetching data: {e}"

    return render(request, 'monitor/process_list.html', {'all_processes': all_processes})


def kill_process(request, host_id, pid):
    """Kill a process on a remote host via SSH."""
    if request.method == "POST":
        host = Host.objects.get(id=host_id)  
        host_ip = host.ip_address
        hostname = host.hostname  
        password = host.password

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(host_ip, username=hostname, password=password)  
            stdin, stdout, stderr = client.exec_command(f"kill -9 {pid}")

            result = stdout.read().decode()
            error = stderr.read().decode()

            client.close()

            if error:
                logging.error(f"Kill process error: {error}")
                return JsonResponse({"success": False, "message": f"Failed to terminate process {pid}. {error}"}, status=400)

            return JsonResponse({"success": True, "message": f"Process {pid} terminated remotely."})

        except Exception as e:
            logging.error(f"Kill process error: {e}")
            return JsonResponse({"success": False, "message": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
