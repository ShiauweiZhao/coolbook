import serial
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
serial_port = '/dev/ttyUSB4'  # 请根据实际情况修改串口名
baud_rate = 115200

ser = None  # 初始化ser变量

try:
    # 打开串口连接
    ser = serial.Serial(serial_port, baud_rate)
    print(f"Connected to {serial_port} at {baud_rate} bps.")

    # 创建一个MAVLink解析器对象
    mav_parser = mavutil.mavlink.MAVLink(ser)

    while True:
        # 读取一个字节的数据
        data = ser.read()

        # 解析收到的字节流
        msg = mav_parser.parse_char(data)

        if msg:
            # 如果成功解析了一条消息，则调用解析函数进行处理
            parse_mavlink_message(msg)

except KeyboardInterrupt:
    print("KeyboardInterrupt: Program terminated.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")
