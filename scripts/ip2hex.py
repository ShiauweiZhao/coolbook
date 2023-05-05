#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import socket

def ip_to_hex(ip_address):
    # 将IP地址转换为32位整数
    ip_int = int.from_bytes(socket.inet_aton(ip_address), byteorder='big')
    # 将32位整数转换为16进制字符串
    hex_str = hex(ip_int).upper()[2:]
    # 在16进制字符串前面添加"0X"
    hex_str = '0X' + hex_str.zfill(8)
    return hex_str

if __name__ == '__main__':
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description='Convert IP address to hex')
    # 添加IP地址参数
    parser.add_argument("-i","--ip", dest="ip_addr", type=str, required=True, help='IP address')
    # 解析命令行参数
    args = parser.parse_args()

    # 转换IP地址为16进制
    hex_str = ip_to_hex(args.ip_addr)
    print(hex_str)
