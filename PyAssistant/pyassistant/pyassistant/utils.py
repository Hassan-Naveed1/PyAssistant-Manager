import paramiko
import logging

def get_process_data_from_remote(host_ip, username, password):
    """Retrieve process data from a remote host via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host_ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command("ps aux")

        process_list = []
        for line in stdout.read().decode().splitlines()[1:]:  # Skip the header line
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
