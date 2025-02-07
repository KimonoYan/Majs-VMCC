import socket
import requests
import subprocess
import json
    
from requests.auth import HTTPBasicAuth

def get_local_ip():
    try:
        # 创建一个UDP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（不会真正发送数据）
        s.connect(("8.8.8.8", 80))  # 使用Google的公共DNS服务器
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"获取本地IP地址失败: {e}")
        return "127.0.0.1"
    finally:
        s.close()


workstation_ip = get_local_ip()  # 本地地址
workstation_port = "8697"     # 默认REST API端口
username = "admin"            # 替换为你设置的用户名
password = "Fanchen3733#"         # 替换为你设置的密码

# 配置信息
base_url = f"http://127.0.0.1:8697/api"
username = "admin"
password = "Fanchen3733#"
vm_name = "Win10-rank-1"  # 修改为你的虚拟机名称

print(base_url)

def get_vm_ip():
    try:
        # 获取所有虚拟机列表
        vms_response = requests.get(
            f"{base_url}/vms",
            auth=HTTPBasicAuth(username, password)
        )
        if vms_response.status_code != 200:
            print(f"获取虚拟机列表失败，状态码：{vms_response.status_code}")
            return None
        vms = vms_response.json()
        
        # 查找目标虚拟机的ID
        vm_id = None
        for vm in vms:
            if vm.get('name') == vm_name:
                vm_id = vm['id']
                break
        if not vm_id:
            print(f"未找到虚拟机：{vm_name}")
            return None
        
        # 获取虚拟机的网络接口信息
        nics_response = requests.get(
            f"{base_url}/vms/{vm_id}/nic",
            auth=HTTPBasicAuth(username, password)
        )
        if nics_response.status_code != 200:
            print(f"获取网络接口失败，状态码：{nics_response.status_code}")
            return None
        nics = nics_response.json()
        
        # 提取IP地址
        for nic in nics:
            ip_addresses = nic.get('ip_addresses', [])
            if ip_addresses:
                return ip_addresses[0].get('ip_address')
        print("未找到IP地址")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        return None



if __name__ == "__main__":
    # 通过 curl 命令调用 REST API
    response = requests.get(f"{base_url}/vms", auth=(username, password))
    if response.status_code == 200:
        try:
            vms = response.json()
            vm_ids = [vm['id'] for vm in vms]
            print(vm_ids)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
    else:
        print(f"Request failed with status code {response.status_code}")
        
        
    # 遍历所有虚拟机ID，获取每个虚拟机的实时IP地址
    for vm_id in vm_ids:
        response2 = requests.get(f"{base_url}/vms/{vm_id}/ip", auth=(username, password))
        if response2.status_code == 200:
            vm_runtime_details = response2.json()
            print(f"VM Runtime Details for {vm_id}: {vm_runtime_details}")  # 调试输出

            vm_name = vm_runtime_details.get('name')
            ip_addresses = vm_runtime_details.get('ip_addresses', [])
            if ip_addresses:
                ip_address = ip_addresses[0].get('ip_address')
            else:
                ip_address = "No IP address found"
            print(f"VM ID: {vm_id}, Name: {vm_name}, IP Address: {ip_address}")
        else:
            print(f"Failed to get runtime details for VM {vm_id} with status code {response2.status_code}")

    
    # 注意：这段代码只能用来查询虚拟机的设置
    # for vm_id in vm_ids:
    #     response2 = requests.get(f"{base_url}/vms/{vm_id}", auth=(username, password))
    #     if response2.status_code == 200:
    #         vm_details = response2.json()
            
    #         print(vm_details)
            
            
    #         vm_name = vm_details.get('name')
    #         ip_addresses = vm_details.get('ip_addresses', [])
    #         if ip_addresses:
    #             ip_address = ip_addresses[0].get('ip_address')
    #         else:
    #             ip_address = "No IP address found"
    #         print(f"VM ID: {vm_id}, Name: {vm_name}, IP Address: {ip_address}")
    #     else:
    #         print(f"Failed to get details for VM {vm_id} with status code {response2.status_code}")
    
    # # result = subprocess.run(["curl", f"{base_url}/vms", "-X", "GET", "--user", f"{username}:{password}"])
    # result = subprocess.run(
    #     ["curl", f"{base_url}/vms", "-X", "GET", "--user", f"{username}:{password}"],
    #     capture_output=True,
    #     text=True
    # )

    # 假设返回的结果是 JSON 格式
    # vms = json.loads(result.stdout)
    # vm_ids = [vm['id'] for vm in vms]


# print("Curl command output:", result.stdout)
    # print(vm_ids)
    
    # print("\n\n\n")
    # print(result)
    
    
    # ip = get_vm_ip()
    # if ip:
    #     print(f"虚拟机 {vm_name} 的IP地址是：{ip}")