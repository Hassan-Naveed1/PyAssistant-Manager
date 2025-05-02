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
matplotlib.use('Agg')  # Since Django runs in a non-GUI environment, I set Matplotlib to use 'Agg' to avoid crashes.

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

        ssh.close()  # Always closing the SSH connection once data is fetched to avoid resource leaks.

        if not output:
            return {'error': "No network data found in /proc/net/dev"}

        # I initialize counters to store the total received and transmitted bytes across all interfaces.
        total_received = 0
        total_transmitted = 0

        # Now, I loop through each network interface found in the output.
        for line in output:
            parts = line.split()
            if len(parts) < 10:
                continue  # If the line is invalid or incomplete, I skip it.

            # Extracting received and transmitted bytes.
            receive_bytes = int(parts[1])  
            transmit_bytes = int(parts[9])  

            # Adding up the total data from all interfaces.
            total_received += receive_bytes
            total_transmitted += transmit_bytes

        # Instead of showing data in KB, I decided to convert everything to MB for better readability.
        receive_mb = total_received / (1024 * 1024)  
        transmit_mb = total_transmitted / (1024 * 1024)  
        total_usage_mb = receive_mb + transmit_mb  

        # Finally, I save the network data to the database so I can visualize it later.
        network_data = NetworkData.objects.create(
            host=host,
            upload_speed=transmit_mb,
            download_speed=receive_mb,
            total_usage=total_usage_mb
        )

        return network_data

    except Exception as e:
        return {'error': str(e)}  # If anything goes wrong, I return the error in JSON format.

def network_view(request, host_id):
    """
    Here, I retrieve the host details from the database based on host_id and get its latest network data.
    If there's an error in fetching the data, I return an error message instead of rendering the page.
    """
    host = get_object_or_404(Host, id=host_id)
    network_data = get_network_data_via_ssh(host)

    if isinstance(network_data, dict) and 'error' in network_data:
        return JsonResponse({'error': network_data['error']})

    # Now, I generate a simple bar graph to display upload and download speeds.
    labels = ["Upload Speed", "Download Speed"]
    speeds = [network_data.upload_speed, network_data.download_speed]
    colors = ['#66b3ff', '#ff6666']

    fig, ax = plt.subplots()
    ax.bar(labels, speeds, color=colors)
    ax.set_ylabel("Speed (MB/s)")
    ax.set_title(f"Network Usage for {host.hostname}")

    # Instead of saving the image to a file, I convert it to a base64 string so it can be embedded in the HTML page.
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    uri = 'data:image/png;base64,' + string
    plt.close(fig)  

    # Finally, I pass the generated graph and network data to the template.
    return render(request, 'network/network_detail.html', {
        'host': host,
        'network_data': network_data,
        'graph': uri
    })
