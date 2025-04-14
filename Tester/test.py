import psutil
import time
import requests
from flask import Flask
from datetime import datetime

# Function to monitor memory usage
def get_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # Convert bytes to MB

# Function to monitor CPU usage
def get_cpu_usage():
    # Return the CPU usage as a percentage
    return psutil.cpu_percent(interval=0.1)

# Function to monitor disk usage
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent  # Percentage of disk usage

# Function to monitor network I/O
def get_network_stats():
    net_stats = psutil.net_io_counters()
    return {
        'bytes_sent': net_stats.bytes_sent / 1024 / 1024,  # Convert to MB
        'bytes_recv': net_stats.bytes_recv / 1024 / 1024   # Convert to MB
    }

# Function to get system uptime
def get_system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = uptime_seconds // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    return f"{int(uptime_hours)} hours, {int(uptime_minutes)} minutes"

# Function to send test requests and calculate response time
def monitor_response_time(url, num_requests=10):
    response_times = []
    start_time = time.time()
    
    for _ in range(num_requests):
        request_start_time = time.time()
        response = requests.get(url)
        request_end_time = time.time()
        response_times.append(request_end_time - request_start_time)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_response_time = sum(response_times) / num_requests
    throughput = num_requests / total_time  # Requests per second

    return avg_response_time, response_times, throughput, total_time

# Generate a performance report
def generate_report():
    url = "http://127.0.0.1:5010/generate"  # URL of the Flask app
    print("Monitoring Flask application...")
    
    # Monitor system metrics before the test
    initial_memory = get_memory_usage()
    initial_cpu = get_cpu_usage()
    initial_disk_usage = get_disk_usage()
    initial_network_stats = get_network_stats()
    initial_uptime = get_system_uptime()

    print(f"Initial memory usage: {initial_memory:.2f} MB")
    print(f"Initial CPU usage: {initial_cpu:.2f}%")
    print(f"Initial disk usage: {initial_disk_usage:.2f}%")
    print(f"Initial network stats (MB sent/received): {initial_network_stats['bytes_sent']:.2f}/{initial_network_stats['bytes_recv']:.2f}")
    print(f"System uptime: {initial_uptime}")

    # Monitor response times and throughput
    num_requests = 10  # Number of test requests
    avg_response_time, response_times, throughput, total_time = monitor_response_time(url, num_requests)
    
    # Monitor system metrics after the test
    final_memory = get_memory_usage()
    final_cpu = get_cpu_usage()
    final_disk_usage = get_disk_usage()
    final_network_stats = get_network_stats()

    print(f"Final memory usage: {final_memory:.2f} MB")
    print(f"Final CPU usage: {final_cpu:.2f}%")
    print(f"Final disk usage: {final_disk_usage:.2f}%")
    print(f"Final network stats (MB sent/received): {final_network_stats['bytes_sent']:.2f}/{final_network_stats['bytes_recv']:.2f}")

    # Print additional details to the console
    print(f"Average Response Time: {avg_response_time:.4f} seconds")
    print(f"Response Times: {response_times}")
    print(f"Throughput: {throughput:.2f} requests/second")
    print(f"Total Time: {total_time:.2f} seconds")

    # Report generation
    report = f"""
    Flask Performance Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    -------------------------------------------------
    Initial Memory Usage: {initial_memory:.2f} MB
    Final Memory Usage: {final_memory:.2f} MB
    Initial CPU Usage: {initial_cpu:.2f}%
    Final CPU Usage: {final_cpu:.2f}%
    Initial Disk Usage: {initial_disk_usage:.2f}%
    Final Disk Usage: {final_disk_usage:.2f}%
    Initial Network Sent: {initial_network_stats['bytes_sent']:.2f} MB
    Final Network Sent: {final_network_stats['bytes_sent']:.2f} MB
    Initial Network Received: {initial_network_stats['bytes_recv']:.2f} MB
    Final Network Received: {final_network_stats['bytes_recv']:.2f} MB
    System Uptime: {initial_uptime}
    Average Response Time: {avg_response_time:.4f} seconds
    Response Times: {response_times}
    Throughput: {throughput:.2f} requests/second
    Total Time: {total_time:.2f} seconds
    """
    
    with open("flask_performance_report.txt", "w") as file:
        file.write(report)
    
    print("Performance report generated: flask_performance_report.txt")

# Run the function if the script is run directly
if __name__ == "__main__":
    generate_report()
