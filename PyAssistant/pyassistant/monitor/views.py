from django.shortcuts import render
from django.http import JsonResponse
import os
import psutil
import datetime
from django.views.decorators.csrf import csrf_exempt  # Import CSRF exemption
from django.utils.decorators import method_decorator
import subprocess



def get_process_data():
    process_list = []

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'create_time']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            cpu_usage = proc.info['cpu_percent'] or 0

            # Calculate execution time safely
            start_time = proc.info['create_time']
            execution_time = "00:00:00" if start_time is None else str(
                datetime.datetime.now() - datetime.datetime.fromtimestamp(start_time)
            ).split('.')[0]  # Keeps HH:MM:SS format

            process_list.append({
                'name': name,
                'pid': pid,
                'execution_time': execution_time,
                'cpu_usage': cpu_usage
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Skip inaccessible processes

    return process_list

def process_list_view(request):
    """ Render the HTML page with process data """
    processes = get_process_data()  # Get process list
    return render(request, 'monitor/process_list.html', {'processes': processes})  # Pass processes to template


def kill_process(request, pid):
    """ Calls process_killer.py to kill a process """
    if request.method == "POST":
        try:
            # Correctly locate the process_killer.py script
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../process_killer.py"))

            # Run the script and capture output
            result = subprocess.run(["python3", script_path, str(pid)], capture_output=True, text=True)

            if result.returncode == 0:
                return JsonResponse({"success": True, "message": f"Process {pid} termination requested."})
            else:
                return JsonResponse({"success": False, "message": f"Failed to terminate process {pid}. Error: {result.stderr}"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
