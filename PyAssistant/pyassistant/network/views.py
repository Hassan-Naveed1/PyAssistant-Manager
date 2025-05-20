import paramiko
import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import NetworkData
from pyassistant.models import Host

import time
import matplotlib

# Here I am setting Matplotlib to use the 'Agg' backend so it can render graphs in a non-GUI environment like Django.
matplotlib.use('Agg')

# Here I am defining a function to fetch network data from a remote host using SSH
def get_network_data_via_ssh(host):
    """
    First, I set up an SSH connection to the remote machine to fetch live network data.
    Instead of relying on one interface like eth0, I dynamically scan all available interfaces.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host.hostname, username=host.username, password=host.password)

        # I run the `cat /proc/net/dev` command to get real-time network data for all interfaces.
        stdin, stdout, stderr = ssh.exec_command("cat /proc/net/dev | tail -n +3")
        output = stdout.read().decode().strip().split("\n")

        ssh.close()  # Here I am closing the SSH connection to avoid resource leaks

        if not output:
            return {'error': "No network data found in /proc/net/dev"}

        total_received = 0
        total_transmitted = 0

        # Here I am processing each interface's data line to extract bytes
        for line in output:
            parts = line.split()
            if len(parts) < 10:
                continue

            receive_bytes = int(parts[1])
            transmit_bytes = int(parts[9])

            total_received += receive_bytes
            total_transmitted += transmit_bytes

        # Here I am converting bytes to MB for readability
        receive_mb = total_received / (1024 * 1024)
        transmit_mb = total_transmitted / (1024 * 1024)
        total_usage_mb = receive_mb + transmit_mb

        # Here I am saving the network data to the database for future access
        network_data = NetworkData.objects.create(
            host=host,
            upload_speed=transmit_mb,
            download_speed=receive_mb,
            total_usage=total_usage_mb
        )

        return network_data

    except Exception as e:
        return {'error': str(e)}

# Here I am defining the Django view to show the network usage and render a graph
def network_view(request, host_id):
    """
    Here, I retrieve the host details from the database based on host_id and get its latest network data.
    If there's an error in fetching the data, I return an error message instead of rendering the page.
    """
    host = get_object_or_404(Host, id=host_id)
    network_data = get_network_data_via_ssh(host)

    if isinstance(network_data, dict) and 'error' in network_data:
        return JsonResponse({'error': network_data['error']})

    # Here I am generating a bar chart to visualize upload and download speeds
    labels = ["Upload Speed", "Download Speed"]
    speeds = [network_data.upload_speed, network_data.download_speed]
    colors = ['#66b3ff', '#ff6666']

    fig, ax = plt.subplots()
    ax.bar(labels, speeds, color=colors)
    ax.set_ylabel("Speed (MB/s)")
    ax.set_title(f"Network Usage for {host.hostname}")

    # Here I am converting the chart to a base64 string for embedding in the template
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    uri = 'data:image/png;base64,' + string
    plt.close(fig)

    # Here I am rendering the network detail template with the graph and latest data
    return render(request, 'network/network_detail.html', {
        'host': host,
        'network_data': network_data,
        'graph': uri
    })
