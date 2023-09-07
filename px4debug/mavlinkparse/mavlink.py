# -*- coding: utf-8 -*-
from pymavlink import mavutil
from datetime import datetime  # 导入datetime模块

def parse_mavlink_message(msg):
    # 获取当前时间戳
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    # 在这里处理解析MAVLink消息的逻辑
    # 这里只是简单地打印时间戳、消息类型和数据负载
    print(f"Timestamp: {timestamp}")
    print("Received MAVLink message:")
    print(f"Message Type: {msg.get_type()}")
    print(f"Payload: {msg.get_payload()}")

# 串口配置
serial_port = '/dev/ttyUSB1'  # 请根据实际情况修改串口名
baud_rate = 115200

ser = None  # 初始化ser变量

try:
    # 打开串口连接
   connection = mavutil.mavlink_connection(serial_device, dialect="efytech",baud=baud_rate)

    while True:
        # 读取一个字节的数据
        message = connection.recv_msg()


       if message is not None:
            # 打印消息类型和消息内容
            # print(f"Received message: {message.get_type()} - {message.to_dict()}")
            parse_mavlink_message(message)

except KeyboardInterrupt:
    print("KeyboardInterrupt: Program terminated.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")
