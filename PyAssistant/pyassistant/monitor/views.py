from django.shortcuts import render
from django.http import JsonResponse
import os
import psutil
import datetime
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
import subprocess



def get_process_data():
    process_list = []
    total_memory = psutil.virtual_memory().total  # Get total system memory for percentage calculation

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'create_time']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'] or "Unknown"
            cpu_usage = proc.info['cpu_percent'] or 0  # CPU Usage
            
            
            memory_usage = 0  
            if 'memory_info' in proc.info and proc.info['memory_info']:
                memory_usage = (proc.info['memory_info'].rss / total_memory) * 100  # Memory Usage Percentage
            
            
            start_time = proc.info['create_time']
            execution_time = "00:00:00" if start_time is None else str(
                datetime.datetime.now() - datetime.datetime.fromtimestamp(start_time)
            ).split('.')[0]  # HH:MM:SS format

            process_list.append({
                'name': name,
                'pid': pid,
                'execution_time': execution_time,
                'cpu_usage': cpu_usage,
                'memory_usage': round(memory_usage, 2)  # Round to 2 decimal places
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Skip inaccessible processes

    # Sort processes alphabetically
    process_list.sort(key=lambda x: x['name'].lower())

    return process_list


def process_list_view(request):
    #This function calls get_process_data() to fetch the process details
    #so i have also a template file as table format meaning it will display the data as i have structured in table 
    """ Render the HTML page with process data """
    processes = get_process_data()  # Get process list
    return render(request, 'monitor/process_list.html', {'processes': processes})  # Pass processes to template


def kill_process(request, pid):
    #Send the request to the file that i have created called process_killer.py to kill a process
    """ Calls process_killer.py to kill a process """
    if request.method == "POST":
        try:

            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../process_killer.py"))


            result = subprocess.run(["python3", script_path, str(pid)], capture_output=True, text=True)

            if result.returncode == 0:
                return JsonResponse({"success": True, "message": f"Process {pid} termination requested."})
            else:
                return JsonResponse({"success": False, "message": f"Failed to terminate process {pid}. Error: {result.stderr}"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
