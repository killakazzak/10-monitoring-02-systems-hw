import os
import json
import time
import datetime

def get_cpu_usage():
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_line = lines[0].split()
    total_cpu_time = sum(int(i) for i in cpu_line[1:])  # Сумма всех значений
    return total_cpu_time

def get_memory_usage():
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    mem_total = int(lines[0].split()[1])  # Total memory
    mem_free = int(lines[1].split()[1])   # Free memory
    mem_used = mem_total - mem_free
    return mem_used, mem_total

def get_disk_usage():
    statvfs = os.statvfs('/')
    total_disk = statvfs.f_blocks * statvfs.f_frsize
    free_disk = statvfs.f_bfree * statvfs.f_frsize
    used_disk = total_disk - free_disk
    return used_disk, total_disk

def get_container_count():
    # Пример для Docker, если он установлен
    try:
        count = int(os.popen('docker ps -q | wc -l').read().strip())
    except Exception:
        count = 0
    return count

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def log_metrics():
    timestamp = int(time.time())
    cpu_usage = get_cpu_usage()
    mem_used, mem_total = get_memory_usage()
    disk_used, disk_total = get_disk_usage()
    container_count = get_container_count()
    uptime = get_uptime()

    log_entry = {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "memory_used": mem_used,
        "memory_total": mem_total,
        "disk_used": disk_used,
        "disk_total": disk_total,
        "container_count": container_count,
        "uptime": uptime
    }

    log_file_path = f"/var/log/{datetime.datetime.now().strftime('%y-%m-%d')}-awesome-monitoring.log"
    with open(log_file_path, 'a') as log_file:
        log_file.write(json.dumps(log_entry) + '\n')

if __name__ == "__main__":
    log_metrics()

