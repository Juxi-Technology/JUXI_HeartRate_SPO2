# -*- coding: utf-8 -*-
'''
  心率血氧监测模块上位机
  功能：
  - 串口选择
  - 波特率选择
  - 连接/断开模块
  - 启动/关闭采集（开灯/关灯）
  - 开始/停止监测
  - 实时显示血氧、心率、温度
'''

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time


class HeartRateOximeterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("心率血氧监测模块上位机")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        self.ser = None
        self.is_connected = False
        self.is_monitoring = False
        self.monitor_thread = None
        self.stop_monitor = False
        
        self.create_widgets()
        self.refresh_ports()
    
    def create_widgets(self):
        # 串口设置区域
        frame_settings = ttk.LabelFrame(self.root, text="串口设置", padding=10)
        frame_settings.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_settings, text="串口:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_combo = ttk.Combobox(frame_settings, width=15, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame_settings, text="刷新", command=self.refresh_ports, width=8).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame_settings, text="波特率:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.baud_combo = ttk.Combobox(frame_settings, width=15, values=["9600", "19200", "38400", "57600", "115200"], state="readonly")
        self.baud_combo.current(0)
        self.baud_combo.grid(row=1, column=1, padx=5, pady=5)
        
        self.connect_btn = ttk.Button(frame_settings, text="连接", command=self.toggle_connection, width=10)
        self.connect_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # 控制区域
        frame_control = ttk.LabelFrame(self.root, text="模块控制", padding=10)
        frame_control.pack(fill=tk.X, padx=10, pady=5)
        
        self.collect_btn = ttk.Button(frame_control, text="启动采集", command=self.toggle_collect, state=tk.DISABLED, width=15)
        self.collect_btn.pack(side=tk.LEFT, padx=10)
        
        self.monitor_btn = ttk.Button(frame_control, text="开始监测", command=self.toggle_monitor, state=tk.DISABLED, width=15)
        self.monitor_btn.pack(side=tk.LEFT, padx=10)
        
        # 数据显示区域
        frame_data = ttk.LabelFrame(self.root, text="实时数据", padding=10)
        frame_data.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 血氧
        ttk.Label(frame_data, text="血氧 (SPO2):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.spo2_label = ttk.Label(frame_data, text="-", font=("Arial", 20, "bold"), foreground="blue")
        self.spo2_label.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(frame_data, text="%", font=("Arial", 12)).grid(row=0, column=2, pady=10, sticky=tk.W)
        
        # 心率
        ttk.Label(frame_data, text="心率 (Heart Rate):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.hr_label = ttk.Label(frame_data, text="-", font=("Arial", 20, "bold"), foreground="green")
        self.hr_label.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(frame_data, text="Times/min", font=("Arial", 12)).grid(row=1, column=2, pady=10, sticky=tk.W)
        
        # 温度
        ttk.Label(frame_data, text="温度 (Temperature):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.temp_label = ttk.Label(frame_data, text="-", font=("Arial", 20, "bold"), foreground="orange")
        self.temp_label.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(frame_data, text="°C", font=("Arial", 12)).grid(row=2, column=2, pady=10, sticky=tk.W)
        
        # 状态
        ttk.Label(frame_data, text="状态:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.status_label = ttk.Label(frame_data, text="未连接", font=("Arial", 10), foreground="gray")
        self.status_label.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # 提示
        frame_tip = ttk.LabelFrame(self.root, text="使用提示", padding=5)
        frame_tip.pack(fill=tk.X, padx=10, pady=5)
        
        tip_text = "1. 接线：VCC->5V, GND->GND, TX->USB-TTL RX, RX->USB-TTL TX\n"
        tip_text += "2. 点击连接后再启动采集\n"
        tip_text += "3. 启动采集后传感器LED会亮起，请将手指放在传感器上"
        ttk.Label(frame_tip, text=tip_text, foreground="gray", justify=tk.LEFT).pack()
    
    def refresh_ports(self):
        """刷新串口列表"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
    
    def calculate_crc(self, data):
        """计算CRC16"""
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for i in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return ((crc & 0x00FF) << 8) | ((crc & 0xFF00) >> 8)
    
    def toggle_connection(self):
        """连接/断开串口"""
        if not self.is_connected:
            port = self.port_combo.get()
            baud = int(self.baud_combo.get())
            
            if not port:
                messagebox.showerror("错误", "请选择串口！")
                return
            
            try:
                self.ser = serial.Serial(port, baud, timeout=0.5)
                self.is_connected = True
                self.connect_btn.config(text="断开")
                self.port_combo.config(state=tk.DISABLED)
                self.baud_combo.config(state=tk.DISABLED)
                self.collect_btn.config(state=tk.NORMAL)
                self.status_label.config(text="已连接，待采集", foreground="blue")
                messagebox.showinfo("成功", "串口连接成功！")
            except Exception as e:
                messagebox.showerror("错误", f"连接失败：{str(e)}")
        else:
            if self.is_monitoring:
                self.toggle_monitor()
            
            if self.ser and self.ser.is_open:
                self.ser.close()
            
            self.is_connected = False
            self.connect_btn.config(text="连接")
            self.port_combo.config(state="readonly")
            self.baud_combo.config(state="readonly")
            self.collect_btn.config(state=tk.DISABLED)
            self.monitor_btn.config(state=tk.DISABLED)
            self.collect_btn.config(text="启动采集")
            self.status_label.config(text="未连接", foreground="gray")
    
    def toggle_collect(self):
        """启动/关闭采集"""
        if not self.is_connected:
            return
        
        if self.collect_btn.cget("text") == "启动采集":
            # 发送开始采集指令
            cmd = [0x20, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x01]
            crc = self.calculate_crc(cmd)
            cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
            
            try:
                self.ser.reset_input_buffer()
                self.ser.write(bytes(cmd))
                time.sleep(0.1)
                
                self.collect_btn.config(text="关闭采集")
                self.monitor_btn.config(state=tk.NORMAL)
                self.status_label.config(text="采集已启动，LED已亮", foreground="green")
            except Exception as e:
                messagebox.showerror("错误", f"启动采集失败：{str(e)}")
        else:
            # 发送停止采集指令
            cmd = [0x20, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x02]
            crc = self.calculate_crc(cmd)
            cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
            
            try:
                self.ser.reset_input_buffer()
                self.ser.write(bytes(cmd))
                time.sleep(0.1)
                
                if self.is_monitoring:
                    self.toggle_monitor()
                
                self.collect_btn.config(text="启动采集")
                self.monitor_btn.config(state=tk.DISABLED)
                self.status_label.config(text="采集已关闭，LED已灭", foreground="orange")
            except Exception as e:
                messagebox.showerror("错误", f"关闭采集失败：{str(e)}")
    
    def toggle_monitor(self):
        """开始/停止监测"""
        if not self.is_connected:
            return
        
        if self.monitor_btn.cget("text") == "开始监测":
            self.stop_monitor = False
            self.is_monitoring = True
            self.monitor_btn.config(text="停止监测")
            self.status_label.config(text="正在监测...", foreground="green")
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
        else:
            self.stop_monitor = True
            self.is_monitoring = False
            self.monitor_btn.config(text="开始监测")
            self.status_label.config(text="监测已停止", foreground="orange")
    
    def monitor_loop(self):
        """监测循环"""
        while not self.stop_monitor and self.is_connected:
            try:
                # 读取心率血氧
                cmd = [0x20, 0x03, 0x00, 0x06, 0x00, 0x04]
                crc = self.calculate_crc(cmd)
                cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
                
                self.ser.reset_input_buffer()
                self.ser.write(bytes(cmd))
                time.sleep(0.1)
                
                if self.ser.in_waiting >= 13:
                    resp = list(self.ser.read(13))
                    if len(resp) >= 11 and resp[0] == 0x20 and resp[1] == 0x03:
                        spo2 = resp[3]
                        heartbeat = (resp[5] << 24) | (resp[6] << 16) | (resp[7] << 8) | resp[8]
                        
                        if spo2 == 0:
                            self.spo2_label.config(text="-1")
                        else:
                            self.spo2_label.config(text=str(spo2))
                        
                        if heartbeat == 0:
                            self.hr_label.config(text="-1")
                        else:
                            self.hr_label.config(text=str(heartbeat))
                
                # 读取温度
                cmd = [0x20, 0x03, 0x00, 0x0A, 0x00, 0x01]
                crc = self.calculate_crc(cmd)
                cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
                
                self.ser.reset_input_buffer()
                self.ser.write(bytes(cmd))
                time.sleep(0.1)
                
                if self.ser.in_waiting >= 7:
                    resp = list(self.ser.read(7))
                    if len(resp) >= 5 and resp[0] == 0x20 and resp[1] == 0x03:
                        temp = resp[3] + resp[4] / 100.0
                        self.temp_label.config(text=f"{temp:.1f}")
                
            except Exception as e:
                print(f"读取错误：{e}")
            
            time.sleep(2)  # 每2秒更新一次
    
    def on_closing(self):
        """关闭窗口"""
        self.stop_monitor = True
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HeartRateOximeterGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
