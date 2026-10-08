import serial
import time
import serial.tools.list_ports

def calculate_crc(data):
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

def list_ports():
    ports = serial.tools.list_ports.comports()
    print("Available serial ports:")
    for port in ports:
        print(f"  {port.device}")
    return [port.device for port in ports]

class BloodOxygenSensor:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=0.5)
        self.dev_addr = 0x20
        self.SPO2 = 0
        self.heartbeat = 0
        
    def send_command(self, cmd):
        self.ser.reset_input_buffer()
        self.ser.write(bytes(cmd))
        time.sleep(0.05)
        
    def read_response(self, expected_bytes=32):
        response = []
        t = time.time()
        while len(response) < expected_bytes and (time.time() - t) < 0.3:
            if self.ser.in_waiting:
                response.append(self.ser.read(1)[0])
            else:
                time.sleep(0.01)
        return response
    
    def begin(self):
        cmd = [self.dev_addr, 0x03, 0x00, 0x02, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self.send_command(cmd)
        resp = self.read_response(7)
        if len(resp) >= 7 and resp[0] == self.dev_addr and resp[1] == 0x03:
            return True
        return False
        
    def sensor_start_collect(self):
        cmd = [self.dev_addr, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self.send_command(cmd)
        time.sleep(0.1)
        
    def sensor_end_collect(self):
        cmd = [self.dev_addr, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x02]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self.send_command(cmd)
        time.sleep(0.1)
        
    def get_heartbeat_SPO2(self):
        cmd = [self.dev_addr, 0x03, 0x00, 0x06, 0x00, 0x04]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self.send_command(cmd)
        resp = self.read_response(13)
        
        if len(resp) >= 11 and resp[0] == self.dev_addr and resp[1] == 0x03:
            self.SPO2 = resp[3]
            if self.SPO2 == 0:
                self.SPO2 = -1
            # Heart rate: resp[5]-resp[8] (4-byte big-endian mode)
            self.heartbeat = (resp[5] << 24) | (resp[6] << 16) | (resp[7] << 8) | resp[8]
            if self.heartbeat == 0:
                self.heartbeat = -1
                
    def get_temperature_c(self):
        cmd = [self.dev_addr, 0x03, 0x00, 0x0A, 0x00, 0x01]
        crc = calculate_crc(cmd)
        cmd.extend([(crc >> 8) & 0xFF, crc & 0xFF])
        self.send_command(cmd)
        resp = self.read_response(7)
        
        if len(resp) >= 7 and resp[0] == self.dev_addr and resp[1] == 0x03:
            temperature = resp[3] + resp[4] / 100.0
            return temperature
        return 0
        
    def close(self):
        self.ser.close()

def main():
    print("=" * 50)
    print("JUXI Blood Oxygen Sensor - Windows Test")
    print("=" * 50)
    
    ports = list_ports()
    if not ports:
        print("\nNo serial ports found! Please check your USB connection.")
        return
    
    print("\nPlease enter the COM port number (e.g., COM3):")
    port = input("> ").strip()
    
    try:
        print(f"\nConnecting to {port} at 9600 baud...")
        sensor = BloodOxygenSensor(port, 9600)
        
        print("Initializing sensor...")
        if not sensor.begin():
            print("Sensor initialization failed!")
            print("Please check:")
            print("  1. TX/RX wiring (cross connection)")
            print("  2. Power supply (3.3V or 5V)")
            print("  3. Baud rate (should be 9600)")
            sensor.close()
            return
        
        print("Sensor initialized successfully!")
        print("\nStarting data collection...")
        sensor.sensor_start_collect()
        print("Sensor LED should be ON now!")
        print("\nPlace your finger on the sensor...\n")
        time.sleep(2)
        
        try:
            while True:
                sensor.get_heartbeat_SPO2()
                temp = sensor.get_temperature_c()
                
                print("-" * 40)
                print(f"SPO2: {sensor.SPO2} %")
                print(f"Heart Rate: {sensor.heartbeat} Times/min")
                print(f"Temperature: {temp:.1f} °C")
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\nStopping...")
            sensor.sensor_end_collect()
            sensor.close()
            print("Sensor turned off.")
            
    except serial.SerialException as e:
        print(f"\nSerial port error: {e}")
        print("Please check:")
        print("  1. The COM port number is correct")
        print("  2. The port is not being used by another program")
        print("  3. You have proper permissions (try running as administrator)")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
