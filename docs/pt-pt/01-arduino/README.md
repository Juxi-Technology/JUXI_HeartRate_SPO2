[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | [Português (BR)](../../pt-br/01-arduino/README.md) | Português (PT) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# Tutorial do Sensor Oxímetro de Ritmo Cardíaco JUXI_HeartRate_SPO2

## Índice
1. [Introdução ao sensor](#introdução-ao-sensor)
2. [Tutorial de Arduino](#tutorial-de-arduino)
3. [Tutorial de Python (Raspberry Pi)](#tutorial-de-python-raspberry-pi)
4. [Perguntas frequentes](#perguntas-frequentes)

---

## Introdução ao sensor

JUXI_HeartRate_SPO2 é um módulo sensor de ritmo cardíaco e oxigénio no sangue baseado no chip MAX30102, com algoritmo incorporado que emite diretamente os valores de ritmo cardíaco e de saturação de oxigénio no sangue.

**Principais características:**

- Medição da saturação de oxigénio no sangue (SPO2)
- Medição do ritmo cardíaco (batimentos por minuto)
- Medição de temperatura incorporada
- Suporta comunicação I2C

---

## Tutorial de Arduino

### 1. Preparação do hardware

| Material necessário |
|---------------------|
| Placa de desenvolvimento Arduino (Uno/Nano/ESP32, etc.) |
| Sensor JUXI_HeartRate_SPO2 |
| Vários fios dupont |
| Cabo de dados USB (para ligar o Arduino ao computador) |

### 2. Instalação da biblioteca

1. Descarregue este ficheiro de biblioteca
2. Copie a pasta `JUXI_HeartRate_SPO2` para o diretório de bibliotecas do Arduino:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Reinicie o Arduino IDE

### 3. Código de exemplo

**Nota: ao carregar o código, ligue apenas o Arduino ao computador, NÃO ligue o módulo oxímetro de ritmo cardíaco ao Arduino!!!**

```cpp
#include "JUXI_HeartRate_SPO2.h"

// I2C address
#define I2C_ADDRESS 0x57

// Create sensor object, I2C mode
JUXI_HeartRate_SPO2_I2C sensor(&Wire, I2C_ADDRESS);

void setup() {
  Serial.begin(9600);

  // Initialize sensor
  while (!sensor.begin()) {
    Serial.println("Sensor initialization failed, please check connection!");
    delay(1000);
  }
  Serial.println("Sensor initialized successfully!");

  // Start data collection
  sensor.sensorStartCollect();
}

void loop() {
  // Read heart rate and blood oxygen data
  sensor.getHeartbeatSPO2();

  // Output blood oxygen saturation
  Serial.print("SPO2: ");
  Serial.print(sensor._sHeartbeatSPO2.SPO2);
  Serial.println(" %");

  // Output heart rate
  Serial.print("Heart Rate: ");
  Serial.print(sensor._sHeartbeatSPO2.Heartbeat);
  Serial.println(" BPM");

  // Read and output temperature
  Serial.print("Onboard Temperature: ");
  Serial.print(sensor.getTemperature_C());
  Serial.println(" °C");

  Serial.println("------------------------");

  // Sensor updates data every 4 seconds
  delay(4000);
}
```

##### Ligação do hardware

Comunicação I2C

| Pino do sensor | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- Coloque o interruptor DIP do módulo oxímetro de ritmo cardíaco na posição I2C!!!
- Utilize o cabo de dados para ligar o Arduino ao computador

#### Resultados da execução:

1. Abra Arduino - Ferramentas - Monitor Série

   Defina a taxa de baud para 9600

![1](../../en/01-arduino/img/1.png)

2. Abra o Assistente de Depuração Série

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Selecione o número da porta série

Defina a taxa de baud para `9600`

Bits de dados `8`, bits de paragem `1`, paridade `NONE`, controlo de fluxo `NONE`

Nas definições de receção e envio, selecione `ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. Descrição da API

| Função | Descrição |
|----------|-------------|
| `begin()` | Inicializa o sensor, devolve verdadeiro/falso |
| `getHeartbeatSPO2()` | Lê os dados de ritmo cardíaco e SPO2, armazenados na estrutura `_sHeartbeatSPO2` |
| `getTemperature_C()` | Lê a temperatura incorporada (Celsius) |
| `sensorStartCollect()` | Inicia a recolha de dados (o LED do sensor acende) |
| `sensorEndCollect()` | Para a recolha de dados (o LED do sensor apaga) |

### 5. Descrição dos dados

- **SPO2 (saturação de oxigénio no sangue)**: intervalo normal 95% - 100%, o valor -1 indica inválido
- **Heartbeat (ritmo cardíaco)**: intervalo normal 60 - 100 BPM, o valor -1 indica inválido
- **Motivos de valores inválidos**: dedo mal posicionado ou dados ainda não estabilizados

---

## Notas de utilização

### Dicas de medição

1. **Posicionamento correto do dedo**
   - Coloque o dedo suavemente sobre o sensor, cobrindo os dois LEDs
   - Não pressione com força para não afetar a circulação sanguínea
   - Mantenha o dedo estável, não o mova

2. **Aguarde a estabilização dos dados**
   - Os valores podem ficar instáveis ao iniciar a medição
   - Recomenda-se aguardar 10-30 segundos até os dados estabilizarem antes de fazer a leitura
   - O sensor atualiza os dados a cada 4 segundos

3. **Requisitos do ambiente**
   - Evite luz forte direta sobre o sensor
   - Mantenha a temperatura ambiente adequada
   - Mantenha-se tranquilo durante a medição

### Interpretação dos dados

| Intervalo de SPO2 | Descrição |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Hipóxia ligeira |
| < 90% | Hipóxia, recomenda-se consulta médica |

| Intervalo de ritmo cardíaco | Descrição |
|-----------------|-------------|
| 60 - 100 BPM | Intervalo normal para adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

---

## Perguntas frequentes

### P1: Falha na inicialização do sensor?

**R:**
1. Verifique se a ligação está correta (SDA para GPIO2/A4, SCL para GPIO3/A5)
2. Confirme se a alimentação está normal (3.3V ou 5V)
3. Utilize o comando `i2cdetect -y 1` para detetar o dispositivo
4. Certifique-se de que o interruptor DIP do sensor está na posição IIC

### P2: Os dados mostram sempre -1?

**R:**
1. Confirme se o dedo está bem colocado sobre o sensor
2. Aguarde alguns segundos até os dados estabilizarem
3. Verifique se `sensorStartCollect()` foi chamado para iniciar a recolha
4. Confirme se o indicador luminoso do sensor está aceso

### P3: Os dados estão imprecisos?

**R:**
1. Certifique-se de que o dedo cobre totalmente a zona ótica do sensor
2. Mantenha o dedo imóvel, não o mova
3. Aguarde mais de 30 segundos até os dados estabilizarem
4. Faça várias medições e calcule a média

### P4: Que placas de desenvolvimento Arduino são suportadas?

**R:** Suportadas:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Outras placas de desenvolvimento compatíveis com o ambiente Arduino

---

## Localização dos ficheiros de exemplo

### Exemplos para Arduino
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```
