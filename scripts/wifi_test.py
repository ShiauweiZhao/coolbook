import argparse
import subprocess
import re
import time
import socket
import struct
import fcntl
import logging
import os
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(filename="wifi_test.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_default_gateway(interface):
    route_output = os.popen("ip route").read()
    match = re.search(r"default via (\d+\.\d+\.\d+\.\d+) dev " + interface, route_output)
    if match:
        return match.group(1)
    else:
        return None


def get_rssi(interface):
    result = subprocess.run(["iwconfig", interface], capture_output=True, text=True)
    match = re.search(r"Signal level=(-?\d+) dBm", result.stdout)
    if match:
        return int(match.group(1))
    else:
        return None

def ping_target(target):
    result = subprocess.run(["ping", "-c", "1", target], capture_output=True, text=True)
    latency_match = re.search(r"time=([\d+\.]+)", result.stdout)
    if latency_match:
        return float(latency_match.group(1))
    else:
        return None

def get_packet_loss_and_latency(target):
    packet_loss = 0
    latency_sum = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(ping_target, [target] * 10))

    for result in results:
        if result is None:
            packet_loss += 1
        else:
            latency_sum += result

    if packet_loss == 10:
        return 100, None

    packet_loss = (packet_loss / 10) * 100
    latency = latency_sum / (10 - packet_loss)

    return packet_loss, latency


def wifi_test(interface):
    gateway_ip = get_default_gateway(interface)

    if gateway_ip is not None:
        while True:
            rssi = get_rssi(interface)
            packet_loss, latency = get_packet_loss_and_latency(gateway_ip)

            if rssi is not None and packet_loss is not None and latency is not None:
                logging.info(f"Gateway IP: {gateway_ip}, RSSI: {rssi} dBm, Packet Loss: {packet_loss}%, Latency: {latency} ms")
            else:
                logging.error("Error getting test data")

            time.sleep(3)  # 每隔 3 秒进行一次测试
    else:
        logging.error("Unable to perform tests, as gateway IP could not be determined")

# 创建命令行解析器
parser = argparse.ArgumentParser(description="Wi-Fi testing script")
parser.add_argument("--interface", dest="interface", default="wlo1", help="name of the Wi-Fi interface")
args = parser.parse_args()

# 开始测试
wifi_test(args.interface)
