import paramiko
import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import StorageData
from pyassistant.models import Host

def get_storage_data_via_ssh(host):
    """
    Connects to a remote machine via SSH and fetches storage information.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        

        ssh.connect(host.hostname, username=host.username, password=host.password)

        # Run `df -h` to get storage details
        stdin, stdout, stderr = ssh.exec_command("df -h --output=size,used,avail / | tail -1")
        output = stdout.read().decode().strip().split()

        if len(output) != 3:
            return {'error': "Unexpected output format from df command"}

        # Convert values to float (removing 'G' for gigabytes)
        total, used, free = map(lambda x: float(x[:-1]), output)

        ssh.close()

        # Save or update storage data in the database
        storage_data, created = StorageData.objects.update_or_create(
            host=host,
            defaults={'total_space': total, 'used_space': used, 'free_space': free}
        )

        return storage_data

    except Exception as e:
        return {'error': str(e)}

def storage_view(request, host_id):
    """
    Retrieves and displays storage data for a given host with a graph.
    """
    host = get_object_or_404(Host, id=host_id)
    storage_data = get_storage_data_via_ssh(host)

    if isinstance(storage_data, dict) and 'error' in storage_data:
        return JsonResponse({'error': storage_data['error']})

    #Generate storage usage graph
    labels = ["Used Space", "Free Space"]
    sizes = [storage_data.used_space, storage_data.free_space]
    colors = ['#ff6666', '#66b3ff']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

    # Convert the graph to an image format
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    uri = 'data:image/png;base64,' + string
    plt.close(fig)

    return render(request, 'storage/storage_detail.html', {
        'host': host,
        'storage_data': storage_data,
        'graph': uri  # Pass the graph URI to the template
    })
