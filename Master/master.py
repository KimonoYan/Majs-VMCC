# 我最近正在设计一个物理机与VMware内部进行通信的中控程序，软件设计这块我有些需求，需要你的帮助。这里重新梳理下大致需求：
# 1）我将使用win11物理机和VMware的诸多win10虚拟机相连，win10虚拟机启动后，等待物理机一侧的指令。
# 2）物理机会发送字符串或流格式的指令数据给虚拟机，并且可以指定哪个窗口接收。虚拟机窗口接收后打印接收到的内容。
# 3）可以用python或者C++实现

 # 这个是物理机的代码，用于发送指令到虚拟机

print("指令发送")
import socket
import requests     # 安装不上

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


def send_instruction(ip, port, message):
    try:
        # 创建一个socket对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 连接到目标虚拟机
            s.connect((ip, port))
            
            # 发送指令
            s.sendall(message.encode('utf-8'))
            print(f"指令已发送到 {ip}:{port}")
    except Exception as e:
        print(f"发送指令失败: {e}")


# 使用 Python 调用 VMware Workstation Pro 的 REST API 获取虚拟机 IP 地址的示例代码
workstation_ip = get_local_ip()  # 本地地址
workstation_port = "8697"     # 默认REST API端口
username = "admin"            # 替换为你设置的用户名
password = "Fanchen3733#"         # 替换为你设置的密码

print("workstation_ip = " + workstation_ip)

# 获取虚拟机列表
def get_vm_list():
    url = f"http://{workstation_ip}:{workstation_port}/rest/vm"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"获取虚拟机列表失败: {response.text}")

# 根据虚拟机名称获取IP地址
def get_vm_ip_by_name(vm_name):
    vms = get_vm_list()
    for vm in vms:
        if vm["name"] == vm_name:
            return vm["guest"]["ip_address"]
    return None

# 示例：获取虚拟机IP地址
try:
    vm_name = "Win10-雀魂-rank-1"  # 替换为你的虚拟机名称
    vm_ip = get_vm_ip_by_name(vm_name)
    if vm_ip:
        print(f"虚拟机 {vm_name} 的IP地址是: {vm_ip}")
    else:
        print(f"未找到虚拟机 {vm_name}")
except Exception as e:
    print(f"发生错误: {e}")

# 示例：发送指令
# vm_ip = get_local_ip()  # 虚拟机的IP地址
# vm_port = 12388          # 虚拟机监听的端口
# instruction = "Hello, VMware!"  # 指令内容

# print("vm_ip = " + vm_ip)
# send_instruction(vm_ip, vm_port, instruction)

# print("指令发送完毕")
