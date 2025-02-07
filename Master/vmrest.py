
import json

def get_vm_ids(response):
    if response.status_code == 200:
        try:
            vms = response.json()
            vm_ids = [vm['id'] for vm in vms]
            print(vm_ids)
            return vm_ids
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return []
    else:
        print(f"Request failed with status code {response.status_code}")
        return []
    

# 一个算法，根据文件路径提取虚拟机名称
# 例如：C:\Users\Administrator\Documents\Virtual Machines\Win10-雀魂-rank-2\Win10-雀魂-rank-2.vmx 则提取出Win10-雀魂-rank-2
def extract_vm_name(file_path):
    import os
    # 获取文件名（带扩展名）
    file_name_with_ext = os.path.basename(file_path)
    # 去掉扩展名
    file_name = os.path.splitext(file_name_with_ext)[0]
    return file_name

    
def get_vm_names(response):
    if response.status_code == 200:
        try:
            vms = response.json()
            vm_path = [vm['path'] for vm in vms]
            vm_name = [extract_vm_name(path) for path in vm_path]
            # print(vm_name)
            return vm_name
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return []
    else:
        print(f"Request failed with status code {response.status_code}")
        return []
    
