import argparse
import subprocess
import time
import logging

# 配置日志
logging.basicConfig(filename="iperf_test.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_iperf_test(server, duration, udp=False, bandwidth=None):
    protocol = "-u" if udp else "-t"
    bandwidth_option = f"-b {bandwidth}M" if bandwidth else ""
    command = f"iperf3 -c {server} {protocol} {duration} {bandwidth_option}"
    logging.info(f"Running command: {command}")
    result = subprocess.run(command.split(), capture_output=True, text=True)
    logging.info(result.stdout)

# 创建命令行解析器
parser = argparse.ArgumentParser(description="iperf testing script")
parser.add_argument("-s", "--server", dest="server", required=True, help="iperf server IP address")
parser.add_argument("-d", "--duration", dest="duration", default="10", help="test duration in seconds")
parser.add_argument("-u", "--udp", dest="udp", action="store_true", help="use UDP instead of TCP")
parser.add_argument("-b", "--bandwidth", dest="bandwidth", type=int, help="set the bandwidth limit in Mbps")
args = parser.parse_args()

# 运行测试
run_iperf_test(args.server, args.duration, args.udp, args.bandwidth)
