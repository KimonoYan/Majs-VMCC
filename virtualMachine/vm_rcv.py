import socket

def receive_instruction(port):
    try:
        # 创建一个socket对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 绑定到指定端口
            s.bind(("0.0.0.0", port))
            s.listen()
            print(f"虚拟机正在监听端口 {port}...")

            # 接收连接
            conn, addr = s.accept()
            with conn:
                print(f"连接已建立: {addr}")
                # 接收指令
                data = conn.recv(1024).decode('utf-8')
                print(f"收到的指令: {data}")
    except Exception as e:
        print(f"接收指令失败: {e}")

# 示例：启动接收端
vm_port = 12388  # 监听的端口
receive_instruction(vm_port)