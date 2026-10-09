[English](../../en/03-windows/README.md) | [Deutsch](../../de/03-windows/README.md) | [Español](../../es/03-windows/README.md) | [Français](../../fr/03-windows/README.md) | [Italiano](../../it/03-windows/README.md) | [日本語](../../ja/03-windows/README.md) | [한국어](../../ko/03-windows/README.md) | Português (BR) | [Português (PT)](../../pt-pt/03-windows/README.md) | [简体中文](../../zh-hans/03-windows/README.md) | [繁體中文](../../zh-hant/03-windows/README.md)

# Sensor Oxímetro de Frequência Cardíaca JUXI - Guia do Usuário Windows

## Índice
1. [Preparação do Hardware](#preparação-do-hardware)
2. [Conexão de Hardware](#conexão-de-hardware)
3. [Configuração do Ambiente de Software](#configuração-do-ambiente-de-software)
4. [Executando o Programa de Exemplo](#executando-o-programa-de-exemplo)
5. [Perguntas Frequentes (FAQ)](#perguntas-frequentes-faq)

---

## Preparação do Hardware

### Materiais Necessários

| Item | Descrição |
|------|-------------|
| Sensor JUXI_HeartRate_SPO2 | Módulo oxímetro de frequência cardíaca |
| Módulo USB para TTL | CH340 / CP2102 / FT232, etc. |
| Fios Dupont | 4 peças (fêmea-fêmea) |
| Computador Windows | Win7/Win10/Win11 |

---

## Conexão de Hardware

### Método de Fiação

| Pino do Sensor | Pino do USB para TTL | Descrição |
|-----------|---------------|-------------|
| **VCC** | 3.3V ou 5V | Positivo da alimentação |
| **GND** | GND | Negativo da alimentação |
| **TX** | RX | Transmissão do sensor → recepção do módulo |
| **RX** | TX | Recepção do sensor → transmissão do módulo |

![Connect PC](../../en/03-windows/Connect%20PC.png)

⚠️ **Dicas Importantes**:

1. **Mude a chave DIP do módulo para a posição UART!!!**
2. **TX e RX devem ser conectados de forma cruzada!**
3. O sensor suporta tanto 3.3V quanto 5V; não conecte a tensão errada
4. Conecte todos os fios primeiro e só depois conecte o USB ao computador

### Diagrama de Fiação

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

## Configuração do Ambiente de Software

### 1. Instalar os Drivers

De acordo com o modelo do chip do seu módulo USB para TTL, instale o driver correspondente:

- **CH340**: https://sparks.gogo.co.nz/ch340.html
- **CP2102**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- **FT232**: https://ftdichip.com/drivers/vcp-drivers/

Após a instalação, conecte o módulo USB para TTL.

### 2. Ver a Porta COM

#### Método 1: Gerenciador de Dispositivos
1. Pressione `Win + X` e selecione "Gerenciador de Dispositivos"
2. Expanda "Portas (COM e LPT)"
3. Verifique o número da porta COM correspondente ao seu USB para TTL (por exemplo, COM3)

#### Método 2: Detecção Automática pelo Programa
Ao executar o programa de exemplo, todas as portas seriais disponíveis serão listadas automaticamente.

### 3. Instalar as Dependências Python

Abra o Prompt de Comando (CMD) ou o PowerShell e execute:

```bash
pip install pyserial
```

---

## Executando o Programa de Exemplo

### Localização dos Arquivos

```
JUXI_HeartRate_SPO2/python/windows/
├── gain_heartbeat_SPO2.py  ← Main program (run this)
├── JUXI_HeartRate_SPO2_Windows.py
├── JUXI_RTU_Windows.py
└── README.md                ← This file
```

### Passos de Execução

1. **Confirme a conexão correta do hardware**
   - VCC → 3.3V/5V
   - GND → GND
   - TX → RX (cruzado)
   - RX → TX (cruzado)

2. **Conecte o USB ao computador**

3. **Execute o programa**
   ```bash
   cd D:\JUXI_HeartRate_SPO2\python\windows
   python gain_heartbeat_SPO2.py
   ```

4. **Siga as instruções**
   
   - O programa listará todas as portas seriais disponíveis
   - Digite o número da sua porta COM (por exemplo, COM3)
   - O programa detectará o sensor automaticamente e iniciará a medição

### Saída Esperada

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

Pressione `Ctrl + C` para encerrar o programa.

---

## Descrição das Funções do Programa

### API Principal

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

## Perguntas Frequentes (FAQ)

### Q1: Não consigo encontrar a porta COM?

**R:**

1. Verifique se o USB para TTL está devidamente conectado
2. Reinstale o driver
3. Tente uma porta USB diferente
4. Verifique se há "Dispositivos desconhecidos" no Gerenciador de Dispositivos

### Q2: A inicialização do sensor falhou?

**R:**

1. Verifique a fiação:
   - O VCC e o GND estão conectados corretamente?
   - **O TX e o RX estão conectados de forma cruzada?** (problema mais comum)
2. Confirme se o baud rate é 9600
3. Verifique se o módulo USB para TTL está funcionando corretamente
4. Reconecte o USB

### Q3: Os dados sempre mostram -1?

**R:**
1. Confirme se o dedo está posicionado corretamente sobre o sensor (cobrindo totalmente a área do LED)
2. Mantenha o dedo firme, não se mova
3. Aguarde alguns segundos para os dados estabilizarem
4. Verifique se o LED do sensor está aceso

### Q4: O LED não acende, mas a comunicação funciona?

**R:**

- Pode ser um problema de hardware no LED, mas o sensor funciona normalmente
- Enquanto os dados estiverem normais, o LED não acender pode ser ignorado

### Q5: A porta serial está ocupada?

**R:**
1. Feche outros softwares seriais (assistente serial, Arduino IDE, etc.)
2. Verifique se outros programas Python estão em execução
3. Reconecte o USB

### Q6: Os dados estão imprecisos?

**R:**
1. Garanta que o dedo cobre totalmente a área óptica do sensor
2. Fique quieto durante a medição, não fale nem se mova
3. Aguarde mais de 30 segundos para os dados estabilizarem
4. Faça várias medições e tire a média

---

## Especificações Técnicas

| Parâmetro | Especificação |
|-----------|--------------|
| Comunicação | UART (nível TTL) |
| Baud Rate | 9600 bps (padrão) |
| Formato de Dados | 8N1 (8 bits de dados, sem paridade, 1 bit de parada) |
| Alimentação | 3.3V / 5V |
| Faixa de SPO2 | 35% - 100% |
| Faixa de Frequência Cardíaca | 30 - 250 BPM |
| Endereço Modbus | 0x20 |

---

## Descrição dos Registradores Modbus

| Endereço do Registrador | Função | Descrição |
|-----------------|----------|-------------|
| 0x02 | ID do Dispositivo | Leitura: retorna 0x0020 |
| 0x06-0x09 | Dados de frequência cardíaca e SPO2 | Leitura: SPO2 + Frequência cardíaca |
| 0x0A | Temperatura | Leitura: temperatura a bordo |
| 0x10 | Controle de coleta | Escrita: 0x0001=iniciar, 0x0002=parar |

---

## Fale Conosco

Para dúvidas ou sugestões, acesse:
- GitHub: https://github.com/Juxi-Technology/JUXI_HeartRate_SPO2
