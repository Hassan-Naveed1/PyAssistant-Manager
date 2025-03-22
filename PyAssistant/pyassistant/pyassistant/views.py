from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Host
from .forms import HostForm
from .utils import get_process_data_from_remote
import os
import paramiko
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Host
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return render(request, 'users/home.html')

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



import os
import paramiko
import traceback
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Host

def install_vnc(request, host_id):
    host = get_object_or_404(Host, id=host_id)
    local_script_path = os.path.join(os.path.dirname(__file__), 'setup_vnc.sh')

    try:
        print(f"🔧 Connecting to {host.ip_address}...")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host.ip_address, username=host.username, password=host.password)

        print("📤 Uploading setup script...")
        sftp = ssh.open_sftp()
        sftp.put(local_script_path, '/tmp/setup_vnc.sh')
        sftp.close()

        print("🚀 Running setup script...")
        # Run the setup script and get outputs using the channel to avoid hanging
        stdin, stdout, stderr = ssh.exec_command('chmod +x /tmp/setup_vnc.sh && bash /tmp/setup_vnc.sh')

        print("📄 STDOUT:")
        for line in iter(stdout.readline, ""):
            print(line.strip())

        print("❌ STDERR:")
        for line in iter(stderr.readline, ""):
            print(line.strip())


        ssh.close()
        messages.success(request, f'✅ VNC setup complete on {host.hostname}')
    except Exception as e:
        error_msg = f'❌ Failed to install VNC on {host.hostname}: {e}'
        print(error_msg)
        traceback.print_exc()
        messages.error(request, error_msg)

    return redirect('host_list')
