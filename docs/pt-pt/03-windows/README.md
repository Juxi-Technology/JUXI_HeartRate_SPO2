[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | [Português (BR)](../../pt-br/03-windows/README.md) | Português (PT) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# Sensor Oxímetro de Ritmo Cardíaco JUXI - Guia do utilizador para Windows

## Índice
1. [Preparação do hardware](#preparação-do-hardware)
2. [Ligação do hardware](#ligação-do-hardware)
3. [Configuração do ambiente de software](#configuração-do-ambiente-de-software)
4. [Execução do programa de exemplo](#execução-do-programa-de-exemplo)
5. [Perguntas frequentes](#perguntas-frequentes)

---

## Preparação do hardware

### Material necessário

| Item | Descrição |
|------|-------------|
| Sensor JUXI_HeartRate_SPO2 | Módulo oxímetro de ritmo cardíaco |
| Módulo USB para TTL | CH340 / CP2102 / FT232, etc. |
| Fios dupont | 4 unidades (fêmea-fêmea) |
| Computador Windows | Win7/Win10/Win11 |

---

## Ligação do hardware

### Método de ligação

| Pino do sensor | Pino do USB para TTL | Descrição |
|-----------|---------------|-------------|
| **VCC** | 3.3V ou 5V | Positivo da alimentação |
| **GND** | GND | Negativo da alimentação |
| **TX** | RX | O sensor transmite → o módulo recebe |
| **RX** | TX | O sensor recebe → o módulo transmite |

![Ligar ao PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Dicas importantes**:

1. **Coloque o interruptor DIP do módulo na posição UART!!!**
2. **O TX e o RX têm de estar ligados de forma cruzada!**
3. O sensor suporta 3.3V e 5V; não ligue uma tensão errada
4. Ligue todos os fios primeiro e só depois ligue o USB ao computador

### Diagrama de ligação

```
Sensor        USB to TTL Module
┌──────┐      ┌──────────┐
│ VCC  │──────│ 3.3V/5V  │
│ GND  │──────│ GND      │
│ TX   │──────│ RX       │  ← Cross connection
│ RX   │──────│ TX       │  ← Cross connection
└──────┘      └──────────┘
```

---

## Configuração do ambiente de software

### 1. Instalar os controladores

Consoante o modelo do chip do seu módulo USB para TTL, instale o controlador correspondente:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

Após a instalação, ligue o módulo USB para TTL.

### 2. Ver a porta COM

#### Método 1: Gestor de Dispositivos
1. Prima `Win + X` e selecione "Gestor de Dispositivos"
2. Expanda "Portas (COM e LPT)"
3. Verifique o número da porta COM correspondente ao seu módulo USB para TTL (por exemplo, COM3)

#### Método 2: deteção automática pelo programa
Ao executar o programa de exemplo, todas as portas série disponíveis são listadas automaticamente.

### 3. Instalar as dependências de Python

Abra a Linha de Comandos (CMD) ou o PowerShell e execute:

```bash
pip install pyserial
```

---

## Execução do programa de exemplo

### Localização dos ficheiros

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Passos de execução

1. **Confirme a ligação correta do hardware**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (cruzada)
   - RX → TX (cruzada)

2. **Ligue o USB ao computador**

3. **Execute o programa**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Siga as instruções**
   
   - O programa lista todas as portas série disponíveis
   - Introduza o número da porta COM (por exemplo, COM3)
   - O programa deteta automaticamente o sensor e inicia a medição

### Saída esperada

```
==================================================
JUXI Blood Oxygen Sensor - Windows Test
==================================================
Available serial ports:
  COM3

Please enter the COM port number (e.g., COM3):
> COM3

Connecting to COM3 at 9600 baud...
Initializing sensor...
Sensor initialized successfully!

Starting data collection...
Sensor LED should be ON now!

Place your finger on the sensor...

----------------------------------------
SPO2: 97 %
Heart Rate: 82 BPM
Temperature: 26.5 °C
----------------------------------------
SPO2: 98 %
Heart Rate: 78 BPM
Temperature: 26.6 °C
...
```

Prima `Ctrl + C` para parar o programa.

---

## Descrição das funções do programa

### API principal

```python
# Create sensor object
sensor = BloodOxygenSensor("COM3", 9600)

# Initialize sensor
sensor.begin()

# Start collection (LED turns on)
sensor.sensor_start_collect()

# Read heart rate and SPO2
sensor.get_heartbeat_SPO2()
print(f"SPO2: {sensor.SPO2}%")
print(f"Heart Rate: {sensor.heartbeat} BPM")

# Read temperature
temp = sensor.get_temperature_c()

# Stop collection (LED turns off)
sensor.sensor_end_collect()

# Close serial port
sensor.close()
```

---

## Perguntas frequentes

### P1: Não encontra a porta COM?

**R:**

1. Verifique se o módulo USB para TTL está bem ligado
2. Reinstale o controlador
3. Experimente outra porta USB
4. Verifique se existem "Dispositivos desconhecidos" no Gestor de Dispositivos

### P2: Falha na inicialização do sensor?

**R:**

1. Verifique a ligação:
   - Se o VCC e o GND estão ligados corretamente
   - **O TX e o RX estão ligados de forma cruzada?** (problema mais comum)
2. Confirme se a taxa de baud é 9600
3. Verifique se o módulo USB para TTL está a funcionar corretamente
4. Volte a ligar o USB

### P3: Os dados mostram sempre -1?

**R:**
1. Confirme se o dedo está bem colocado sobre o sensor (cobrindo totalmente a zona do LED)
2. Mantenha o dedo estável, não o mova
3. Aguarde alguns segundos até os dados estabilizarem
4. Verifique se o LED do sensor está aceso

### P4: O LED não acende, mas a comunicação funciona?

**R:**

- Pode ser um problema de hardware com o LED, mas o sensor funciona normalmente
- Desde que os dados estejam normais, o facto de o LED não acender pode ser ignorado

### P5: A porta série está ocupada?

**R:**
1. Feche outro software de porta série (assistente série, Arduino IDE, etc.)
2. Verifique se há outros programas Python em execução
3. Volte a ligar o USB

### P6: Os dados estão imprecisos?

**R:**
1. Certifique-se de que o dedo cobre totalmente a zona ótica do sensor
2. Mantenha-se tranquilo durante a medição, não fale nem se mova
3. Aguarde mais de 30 segundos até os dados estabilizarem
4. Faça várias medições e calcule a média

---

## Especificações técnicas

| Parâmetro | Especificação |
|-----------|--------------|
| Comunicação | UART (nível TTL) |
| Taxa de baud | 9600 bps (predefinida) |
| Formato de dados | 8N1 (8 bits de dados, sem paridade, 1 bit de paragem) |
| Alimentação | 3.3V / 5V |
| Intervalo de SPO2 | 35% - 100% |
| Intervalo de ritmo cardíaco | 30 - 250 BPM |
| Endereço Modbus | 0x20 |

---

## Descrição dos registos Modbus

| Endereço do registo | Função | Descrição |
|-----------------|----------|-------------|
| 0x02 | ID do dispositivo | Leitura: devolve 0x0020 |
| 0x06-0x09 | Dados de ritmo cardíaco e SPO2 | Leitura: SPO2 + ritmo cardíaco |
| 0x0A | Temperatura | Leitura: temperatura incorporada |
| 0x10 | Controlo da recolha | Escrita: 0x0001=iniciar, 0x0002=parar |

---

## Contacte-nos

Para questões ou sugestões, visite:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2
