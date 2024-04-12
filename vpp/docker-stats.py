import subprocess
import threading

def gather_stats(container_name, output_file):
    command = 'docker stats ' + container_name + ' --no-stream --format "{{.Container}} {{.CPUPerc}} {{.MemUsage}} {{.MemPerc}} {{.NetIO}} {{.BlockIO}} {{.PIDs}}"'
    #command = f'docker stats {container_name} --no-stream --format "{{{{.Container}}}} {{{{.CPUPerc}}}} {{{{.MemUsage}}}} {{{{.MemPerc}}}} {{{{.NetIO}}}} {{{{.BlockIO}}}} {{{{.PIDs}}}}"'
    #command = f"docker stats {container_name} --no-stream --format \"{{{{.Container}}}} {{{{.CPUPerc}}}} {{{{.MemUsage}}}} {{{{.MemPerc}}}} {{{{.NetIO}}}} {{{{.BlockIO}}}} {{{{.PIDs}}}}\""
    #command = f'docker stats {container_name} --no-stream --format "{{.Container}} {{.CPUPerc}} {{.MemUsage}} {{.MemPerc}} {{.NetIO}} {{.BlockIO}} {{.PIDs}}"'
    stats = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    print(stats)
    with open(output_file, 'a') as file:
        file.write(stats + '\n')

    # Schedule the next stats gathering
    threading.Timer(0.5, gather_stats, args=[container_name, output_file]).start()

def main():
    container_name = "vpp-upf"
    output_file = "docker_stats.txt"

    # Write the header to the output file
    header = "CONTAINER           CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS\n"
    with open(output_file, 'w') as file:
        file.write(header)

    # Start gathering stats
    gather_stats(container_name, output_file)

if __name__ == "__main__":
    main()










