
import socket
import requests
import subprocess
import json
    
from requests.auth import HTTPBasicAuth

import vmrest
import gui

# 配置信息
vmrest_port = "8697"
base_url = f"http://127.0.0.1:{vmrest_port}/api"
username = "admin"
password = "Fanchen3733#"

class Vmachine:
    def __init__(self, vm_id, vm_name=None, ip_address=None, note=None, group=None):
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.ip_address = ip_address
        self.note = note
        self.group = group

    def __repr__(self):
        return f"Vmachine(vm_id={self.vm_id}, vm_name={self.vm_name}, ip_address={self.ip_address}, note={self.note}, group={self.group})"


if __name__ == "__main__":
    # 打开一个cmd窗口，执行 vmrest.exe
    
    # 通过 curl 命令调用 REST API
    response = requests.get(f"{base_url}/vms", auth=(username, password))
    

    # 这两个变量要根据下标一一对应，有点蛋疼
    vm_ids = vmrest.get_vm_ids(response)
    vm_paths = vmrest.get_vm_names(response)

    # 遍历所有虚拟机ID，获取每个虚拟机的实时IP地址
    vmachines = []
    i = 0
    for vm_id in vm_ids:
        response_ips = requests.get(f"{base_url}/vms/{vm_id}/ip", auth=(username, password))
        if response_ips.status_code == 200:
            vm_runtime_details = response_ips.json()
            
            print(f"VM Runtime Details for {vm_id}: {vm_runtime_details}")  # 调试输出
            ip_addresses = vm_runtime_details.get('ip')
            if ip_addresses:
                ip_address = ip_addresses
            else:
                ip_address = "No IP address found"
            
            vm_name = vm_paths[i]
            vmachine = Vmachine(vm_id, vm_name, ip_address)
            vmachines.append(vmachine)
            i = i + 1
            
        else:
            print(f"Failed to get runtime details for VM {vm_id} with status code {response_ips.status_code}")

    # 打印所有虚拟机信息
    for vmachine in vmachines:
        print(vmachine)
     
     
    gui.create_gui(vmachines)
     


    # 通过点击虚拟机名称，可以获取虚拟机的IP地址
    # 通过点击虚拟机的IP地址，可以发送指令到虚拟机

        
        
    # for vm_id in vm_ids:
    #     response_ips = requests.get(f"{base_url}/vms/{vm_id}/ip", auth=(username, password))
    #     if response_ips.status_code == 200:
    #         vm_runtime_details = response_ips.json()
    #         print(f"VM Runtime Details for {vm_id}: {vm_runtime_details}")  # 调试输出

    #         vm_name = vm_runtime_details.get('name')
    #         ip_addresses = vm_runtime_details.get('ip_addresses', [])
    #         if ip_addresses:
    #             ip_address = ip_addresses[0].get('ip_address')
    #         else:
    #             ip_address = "No IP address found"
    #         print(f"VM ID: {vm_id}, Name: {vm_name}, IP Address: {ip_address}")
    #     else:
    #         print(f"Failed to get runtime details for VM {vm_id} with status code {response_ips.status_code}")