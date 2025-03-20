import paramiko

def kill_process(host_ip, username, password, pid):
    """Kills a process on a remote machine via SSH for both Windows & Linux."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, username=username, password=password)

        # Detect remote OS
        stdin, stdout, stderr = client.exec_command("uname")
        os_type = stdout.read().decode().strip()

        if os_type == "Linux":
            kill_command = f"sudo kill -9 {pid}"
        else:
            kill_command = f"taskkill /F /PID {pid}"

        stdin, stdout, stderr = client.exec_command(kill_command)
        error = stderr.read().decode().strip()

        client.close()

        if error:
            return f"Error: {error}"
        return f"Process {pid} killed successfully on {host_ip}."

    except Exception as e:
        return f"Error: {str(e)}"
