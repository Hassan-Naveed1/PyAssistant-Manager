from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Host
from .forms import HostForm
from .utils import get_process_data_from_remote


def add_host(request):
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            print("Form is valid. Saving host...")
            form.save()
            return redirect('host_list')  
        else:
            print("Form is not valid:", form.errors)
    else:
        form = HostForm()
    
    return render(request, 'pyassistant/add_host.html', {'form': form})

def host_list(request):
    hosts = Host.objects.all()
    return render(request, 'pyassistant/host_list.html', {'hosts': hosts})

def view_host_processes(request, host_id):
    """View to show processes for a specific host."""
    try:
        host = Host.objects.get(id=host_id)  
        processes = get_process_data_from_remote(host.ip_address, host.hostname, host.password)
    except Host.DoesNotExist:
        return JsonResponse({"success": False, "message": "Host not found."}, status=404)

    return render(request, 'monitor/host_processes.html', {'host': host, 'processes': processes})
