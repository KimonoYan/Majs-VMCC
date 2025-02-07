# 生成一个GUI，采用列表显示所有vmachines中的虚拟机信息
import tkinter as tk
from tkinter import ttk  

def create_gui(vmachines):
    root = tk.Tk()
    root.title("VMachines")

    tree = ttk.Treeview(root, columns=("ID", "Name", "IP Address"), show='headings')
    tree.heading("ID", text="VM ID")
    tree.heading("Name", text="VM Name")
    tree.heading("IP Address", text="IP Address")

    for vm in vmachines:
        tree.insert("", "end", values=(vm.vm_id, vm.vm_name, vm.ip_address))

    tree.pack(expand=True, fill='both')
    root.mainloop()
    