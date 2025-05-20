import paramiko
import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import StorageData
from pyassistant.models import Host
from django.contrib.auth.decorators import login_required

# Here I am connecting to the remote host via SSH to collect storage information

def get_storage_data_via_ssh(host):
    try:
        print(f"DEBUG: Trying to connect to {host.hostname}")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        import socket
        try:
            resolved_ip = socket.gethostbyname(host.hostname)
            print(f"DEBUG: Resolved IP Address: {resolved_ip}")
        except socket.gaierror as e:
            print(f"DEBUG: Hostname resolution failed: {e}")
            return {'error': f"Invalid hostname: {host.hostname}"}

        ssh.connect(host.hostname, username=host.username, password=host.password)

        stdin, stdout, stderr = ssh.exec_command("df -h --output=size,used,avail / | tail -1")
        output = stdout.read().decode().strip().split()

        if len(output) != 3:
            return {'error': "Unexpected output format from df command"}

        total, used, free = map(lambda x: float(x[:-1]), output)

        ssh.close()

        # Here I am saving the storage data in the database or updating if already exists
        storage_data, created = StorageData.objects.update_or_create(
            host=host,
            defaults={'total_space': total, 'used_space': used, 'free_space': free}
        )

        return storage_data

    except Exception as e:
        return {'error': str(e)}



# Here I am rendering the storage data and pie chart in the template

def storage_view(request, host_id):
    host = get_object_or_404(Host, id=host_id)
    storage_data = get_storage_data_via_ssh(host)

    if isinstance(storage_data, dict) and 'error' in storage_data:
        return JsonResponse({'error': storage_data['error']})

    labels = ["Used Space", "Free Space"]
    sizes = [storage_data.used_space, storage_data.free_space]
    colors = ['#ff6666', '#66b3ff']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')

    # Here I am converting the pie chart into a base64 string to embed in HTML
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    uri = 'data:image/png;base64,' + string
    plt.close(fig)

    return render(request, 'storage/storage_detail.html', {
        'host': host,
        'storage_data': storage_data,
        'graph': uri
    })
