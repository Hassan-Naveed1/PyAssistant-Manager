from django.shortcuts import render
from django.http import JsonResponse
import psutil

def network_usage(request):
    """Initial page load with template rendering"""
    return render(request, 'network/network_usage.html')

def get_network_usage_data(request):
    """API endpoint to fetch real-time network usage per process"""
    processes = []

    for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'] or "Unknown"
            username = proc.info['username']
            
            # Get network connections for each process
            connections = proc.connections(kind='inet')
            bytes_sent = sum(conn.raddr[1] if conn.raddr else 0 for conn in connections)
            bytes_received = sum(conn.laddr[1] if conn.laddr else 0 for conn in connections)

            process_stats = {
                'pid': pid,
                'name': name,
                'username': username,
                'bytes_sent': bytes_sent,
                'bytes_received': bytes_received,
                'connections': len(connections)
            }
            processes.append(process_stats)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Sort alphabetically by process name
    processes.sort(key=lambda x: x['name'].lower())

    return JsonResponse({'processes': processes})
