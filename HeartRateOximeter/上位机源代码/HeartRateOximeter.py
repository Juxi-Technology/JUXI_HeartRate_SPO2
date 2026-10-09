# -*- coding: utf-8 -*-
'''
  Heart Rate & Blood Oxygen Monitor - GUI (English / 中文)
  Features:
  - Language switch (English / 中文), English by default
  - Serial port selection
  - Baud rate selection
  - Connect / disconnect the module
  - Start / stop collection (LED on / off)
  - Start / stop monitoring
  - Real-time display of SPO2, heart rate and temperature
'''

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time


TEXTS = {
    "en": {
        "title": "Heart Rate Oximeter Module",
        "lang_label": "Language:",
        "sec_settings": "Serial Port Settings",
        "port": "Port:",
        "baud": "Baud Rate:",
        "refresh": "Refresh",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "sec_control": "Module Control",
        "start_collect": "Start Collection",
        "stop_collect": "Stop Collection",
        "start_monitor": "Start Monitoring",
        "stop_monitor": "Stop Monitoring",
        "sec_data": "Real-time Data",
        "spo2": "Blood Oxygen (SPO2):",
        "hr": "Heart Rate:",
        "hr_unit": "BPM",
        "temp": "Temperature:",
        "status": "Status:",
        "sec_tip": "Usage Tips",
        "tip": "1. Wiring: VCC->5V, GND->GND, TX->RX, RX->TX\n"
               "2. Click Connect before starting collection\n"
               "3. LED turns on after start; place finger on the sensor",
        "st_disconnected": "Disconnected",
        "st_connected": "Connected, ready to collect",
        "st_collecting": "Collecting, LED is on",
        "st_collect_stopped": "Collection stopped, LED is off",
        "st_monitoring": "Monitoring...",
        "st_monitor_stopped": "Monitoring stopped",
        "msg_error": "Error",
        "msg_success": "Success",
        "select_port": "Please select a serial port!",
        "connect_ok": "Serial port connected!",
        "connect_fail": "Connection failed: ",
        "collect_start_fail": "Failed to start collection: ",
        "collect_stop_fail": "Failed to stop collection: ",
        "read_error": "Read error: ",
    },
    "zh": {
        "title": "心率血氧监测模块上位机",
        "lang_label": "语言:",
        "sec_settings": "串口设置",
        "port": "串口:",
        "baud": "波特率:",
        "refresh": "刷新",
        "connect": "连接",
        "disconnect": "断开",
        "sec_control": "模块控制",
        "start_collect": "启动采集",
        "stop_collect": "关闭采集",
        "start_monitor": "开始监测",
        "stop_monitor": "停止监测",
        "sec_data": "实时数据",
        "spo2": "血氧 (SPO2):",
        "hr": "心率 (Heart Rate):",
        "hr_unit": "次/分",
        "temp": "温度 (Temperature):",
        "status": "状态:",
        "sec_tip": "使用提示",
        "tip": "1. 接线：VCC->5V, GND->GND, TX->USB-TTL RX, RX->USB-TTL TX\n"
               "2. 点击连接后再启动采集\n"
               "3. 启动采集后传感器LED会亮起，请将手指放在传感器上",
        "st_disconnected": "未连接",
        "st_connected": "已连接，待采集",
        "st_collecting": "采集已启动，LED已亮",
        "st_collect_stopped": "采集已关闭，LED已灭",
        "st_monitoring": "正在监测...",
        "st_monitor_stopped": "监测已停止",
        "msg_error": "错误",
        "msg_success": "成功",
        "select_port": "请选择串口！",
        "connect_ok": "串口连接成功！",
        "connect_fail": "连接失败：",
        "collect_start_fail": "启动采集失败：",
        "collect_stop_fail": "关闭采集失败：",
        "read_error": "读取错误：",
    },
}

LANGUAGES = [("en", "English"), ("zh", "中文")]


class HeartRateOximeterGUI:
    def __init__(self, root):
        self.root = root
        # 尺寸交给 Tk 按内容自适应，避免不同 DPI/字体下出现裁切
        self.root.resizable(False, False)

        self.lang = "en"

        self.ser = None
        self.is_connected = False
        self.is_collecting = False
        self.is_monitoring = False
        self.monitor_thread = None
        self.stop_monitor = False

        self.status_key = "st_disconnected"
        self.status_color = "gray"

        self.create_widgets()
        self.retranslate()
        self.refresh_ports()

    def t(self, key):
        return TEXTS[self.lang].get(key, key)

    def create_widgets(self):
        # 语言切换 / Language switch
        frame_lang = ttk.Frame(self.root)
        frame_lang.pack(fill=tk.X, padx=10, pady=(8, 0))

        self.lang_label = ttk.Label(frame_lang, text="")
        self.lang_label.pack(side=tk.LEFT)

        self.lang_combo = ttk.Combobox(frame_lang, width=10, state="readonly",
                                       values=[name for _, name in LANGUAGES])
        self.lang_combo.current(0)
        self.lang_combo.pack(side=tk.RIGHT)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_lang_change)

        # 串口设置区域
        self.frame_settings = ttk.LabelFrame(self.root, text="", padding=10)
        self.frame_settings.pack(fill=tk.X, padx=10, pady=5)

        self.port_label = ttk.Label(self.frame_settings, text="")
        self.port_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_combo = ttk.Combobox(self.frame_settings, width=15, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)

        self.refresh_btn = ttk.Button(self.frame_settings, text="", command=self.refresh_ports, width=8)
        self.refresh_btn.grid(row=0, column=2, padx=5, pady=5)

        self.baud_label = ttk.Label(self.frame_settings, text="")
        self.baud_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.baud_combo = ttk.Combobox(self.frame_settings, width=15, values=["9600", "19200", "38400", "57600", "115200"], state="readonly")
        self.baud_combo.current(0)
        self.baud_combo.grid(row=1, column=1, padx=5, pady=5)

        self.connect_btn = ttk.Button(self.frame_settings, text="", command=self.toggle_connection, width=10)
        self.connect_btn.grid(row=1, column=2, padx=5, pady=5)

        # 控制区域
        self.frame_control = ttk.LabelFrame(self.root, text="", padding=10)
        self.frame_control.pack(fill=tk.X, padx=10, pady=5)

        self.collect_btn = ttk.Button(self.frame_control, text="", command=self.toggle_collect, state=tk.DISABLED, width=16)
        self.collect_btn.pack(side=tk.LEFT, padx=8)

        self.monitor_btn = ttk.Button(self.frame_control, text="", command=self.toggle_monitor, state=tk.DISABLED, width=16)
        self.monitor_btn.pack(side=tk.LEFT, padx=8)

        # 提示（先于数据区打包，固定自身高度，避免被后面 expand 的数据区挤扁）
        self.frame_tip = ttk.LabelFrame(self.root, text="", padding=5)
        self.frame_tip.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.tip_label = ttk.Label(self.frame_tip, text="", foreground="gray", justify=tk.LEFT, wraplength=460)
        self.tip_label.pack(anchor=tk.W, fill=tk.X)

        # 数据显示区域
        self.frame_data = ttk.LabelFrame(self.root, text="", padding=10)
        self.frame_data.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 血氧
        self.spo2_name = ttk.Label(self.frame_data, text="", font=("Arial", 12))
        self.spo2_name.grid(row=0, column=0, padx=10, pady=6, sticky=tk.W)
        self.spo2_label = ttk.Label(self.frame_data, text="-", font=("Arial", 20, "bold"), foreground="blue")
        self.spo2_label.grid(row=0, column=1, padx=10, pady=6)
        ttk.Label(self.frame_data, text="%", font=("Arial", 12)).grid(row=0, column=2, pady=6, sticky=tk.W)

        # 心率
        self.hr_name = ttk.Label(self.frame_data, text="", font=("Arial", 12))
        self.hr_name.grid(row=1, column=0, padx=10, pady=6, sticky=tk.W)
        self.hr_label = ttk.Label(self.frame_data, text="-", font=("Arial", 20, "bold"), foreground="green")
        self.hr_label.grid(row=1, column=1, padx=10, pady=6)
        self.hr_unit_label = ttk.Label(self.frame_data, text="", font=("Arial", 12))
        self.hr_unit_label.grid(row=1, column=2, pady=6, sticky=tk.W)

        # 温度
        self.temp_name = ttk.Label(self.frame_data, text="", font=("Arial", 12))
        self.temp_name.grid(row=2, column=0, padx=10, pady=6, sticky=tk.W)
        self.temp_label = ttk.Label(self.frame_data, text="-", font=("Arial", 20, "bold"), foreground="orange")
        self.temp_label.grid(row=2, column=1, padx=10, pady=6)
        ttk.Label(self.frame_data, text="°C", font=("Arial", 12)).grid(row=2, column=2, pady=6, sticky=tk.W)

        # 状态
        self.status_name = ttk.Label(self.frame_data, text="", font=("Arial", 12))
        self.status_name.grid(row=3, column=0, padx=10, pady=6, sticky=tk.W)
        self.status_label = ttk.Label(self.frame_data, text="", font=("Arial", 10), foreground="gray")
        self.status_label.grid(row=3, column=1, columnspan=2, padx=10, pady=6, sticky=tk.W)

    def retranslate(self):
        """按当前语言刷新所有界面文字（不改变程序状态）"""
        self.root.title(self.t("title"))

        self.lang_label.config(text=self.t("lang_label"))
        self.frame_settings.config(text=self.t("sec_settings"))
        self.port_label.config(text=self.t("port"))
        self.baud_label.config(text=self.t("baud"))
        self.refresh_btn.config(text=self.t("refresh"))
        self.connect_btn.config(text=self.t("disconnect") if self.is_connected else self.t("connect"))

        self.frame_control.config(text=self.t("sec_control"))
        self.collect_btn.config(text=self.t("stop_collect") if self.is_collecting else self.t("start_collect"))
        self.monitor_btn.config(text=self.t("stop_monitor") if self.is_monitoring else self.t("start_monitor"))

        self.frame_data.config(text=self.t("sec_data"))
        self.spo2_name.config(text=self.t("spo2"))
        self.hr_name.config(text=self.t("hr"))
        self.hr_unit_label.config(text=self.t("hr_unit"))
        self.temp_name.config(text=self.t("temp"))
        self.status_name.config(text=self.t("status"))

        self.frame_tip.config(text=self.t("sec_tip"))
        self.tip_label.config(text=self.t("tip"))

        self.status_label.config(text=self.t(self.status_key), foreground=self.status_color)

    def on_lang_change(self, event=None):
        self.lang = LANGUAGES[self.lang_combo.current()][0]
        self.retranslate()

    def set_status(self, key, color):
        """记录状态文字，以便切换语言时正确重绘"""
        self.status_key = key
        self.status_color = color
        self.status_label.config(text=self.t(key), foreground=color)

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
                messagebox.showerror(self.t("msg_error"), self.t("select_port"))
                return

            try:
                self.ser = serial.Serial(port, baud, timeout=0.5)
                self.is_connected = True
                self.connect_btn.config(text=self.t("disconnect"))
                self.port_combo.config(state=tk.DISABLED)
                self.baud_combo.config(state=tk.DISABLED)
                self.collect_btn.config(state=tk.NORMAL)
                self.set_status("st_connected", "blue")
                messagebox.showinfo(self.t("msg_success"), self.t("connect_ok"))
            except Exception as e:
                messagebox.showerror(self.t("msg_error"), self.t("connect_fail") + str(e))
        else:
            if self.is_monitoring:
                self.toggle_monitor()

            if self.ser and self.ser.is_open:
                self.ser.close()

            self.is_connected = False
            self.is_collecting = False
            self.connect_btn.config(text=self.t("connect"))
            self.port_combo.config(state="readonly")
            self.baud_combo.config(state="readonly")
            self.collect_btn.config(state=tk.DISABLED)
            self.monitor_btn.config(state=tk.DISABLED)
            self.collect_btn.config(text=self.t("start_collect"))
            self.set_status("st_disconnected", "gray")

    def toggle_collect(self):
        """启动/关闭采集"""
        if not self.is_connected:
            return

        if not self.is_collecting:
            # 发送开始采集指令
            cmd = [0x20, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x01]
            crc = self.calculate_crc(cmd)
            cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])

            try:
                self.ser.reset_input_buffer()
                self.ser.write(bytes(cmd))
                time.sleep(0.1)

                self.is_collecting = True
                self.collect_btn.config(text=self.t("stop_collect"))
                self.monitor_btn.config(state=tk.NORMAL)
                self.set_status("st_collecting", "green")
            except Exception as e:
                messagebox.showerror(self.t("msg_error"), self.t("collect_start_fail") + str(e))
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

                self.is_collecting = False
                self.collect_btn.config(text=self.t("start_collect"))
                self.monitor_btn.config(state=tk.DISABLED)
                self.set_status("st_collect_stopped", "orange")
            except Exception as e:
                messagebox.showerror(self.t("msg_error"), self.t("collect_stop_fail") + str(e))

    def toggle_monitor(self):
        """开始/停止监测"""
        if not self.is_connected:
            return

        if not self.is_monitoring:
            self.stop_monitor = False
            self.is_monitoring = True
            self.monitor_btn.config(text=self.t("stop_monitor"))
            self.set_status("st_monitoring", "green")
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
        else:
            self.stop_monitor = True
            self.is_monitoring = False
            self.monitor_btn.config(text=self.t("start_monitor"))
            self.set_status("st_monitor_stopped", "orange")

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
                print(self.t("read_error") + str(e))

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
