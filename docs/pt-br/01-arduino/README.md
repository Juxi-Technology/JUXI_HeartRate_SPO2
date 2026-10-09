[English](../../en/01-arduino/README.md) | [Deutsch](../../de/01-arduino/README.md) | [Español](../../es/01-arduino/README.md) | [Français](../../fr/01-arduino/README.md) | [Italiano](../../it/01-arduino/README.md) | [日本語](../../ja/01-arduino/README.md) | [한국어](../../ko/01-arduino/README.md) | Português (BR) | [Português (PT)](../../pt-pt/01-arduino/README.md) | [简体中文](../../zh-hans/01-arduino/README.md) | [繁體中文](../../zh-hant/01-arduino/README.md)

# Tutorial do Sensor Oxímetro de Frequência Cardíaca JUXI_HeartRate_SPO2

## Índice
1. [Introdução ao Sensor](#introdução-ao-sensor)
2. [Tutorial do Arduino](#tutorial-do-arduino)
3. [Tutorial Python (Raspberry Pi)](#tutorial-python-raspberry-pi)
4. [Perguntas Frequentes (FAQ)](#perguntas-frequentes-faq)

---

## Introdução ao Sensor

JUXI_HeartRate_SPO2 é um módulo sensor de frequência cardíaca e oxigenação do sangue (SpO2) baseado no chip MAX30102, com algoritmo embarcado que fornece diretamente os valores de frequência cardíaca e saturação de oxigênio no sangue.

**Principais Características:**

- Medição da saturação de oxigênio no sangue (SPO2)
- Medição da frequência cardíaca (batimentos por minuto)
- Medição de temperatura a bordo
- Suporte à comunicação I2C

---

## Tutorial do Arduino

### 1. Preparação do Hardware

| Materiais Necessários |
|-------------------|
| Placa de desenvolvimento Arduino (Uno/Nano/ESP32, etc.) |
| Sensor JUXI_HeartRate_SPO2 |
| Alguns fios dupont |
| Cabo de dados USB (para conectar o Arduino ao computador) |

### 2. Instalação da Biblioteca

1. Baixe o arquivo desta biblioteca
2. Copie a pasta `JUXI_HeartRate_SPO2` para o diretório de bibliotecas do seu Arduino:
   - Windows: `C:\Users\Username\Documents\Arduino\libraries\`
   - Mac: `~/Documents/Arduino/libraries/`
   - Linux: `~/Arduino/libraries/`
3. Reinicie a Arduino IDE

### 3. Código de Exemplo

**Atenção: Ao enviar o código, conecte apenas o Arduino ao computador; NÃO conecte o módulo oxímetro de frequência cardíaca ao Arduino!!!**

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

##### Conexão de Hardware

Comunicação I2C

| Pino do Sensor | Arduino |
|-----------|---------|
| VCC       | 5V/3.3V |
| GND       | GND     |
| SDA       | SDA/A4  |
| SCL       | SCL/A5  |

![IIC](../../en/01-arduino/img/IIC.png)

![8](../../en/01-arduino/img/8.png)

- Mude a chave DIP do módulo oxímetro de frequência cardíaca para a posição I2C!!!
- Use o cabo de dados para conectar o Arduino ao computador

#### Resultados da Execução:

1. Abra Arduino - Ferramentas - Monitor Serial

   Defina o baud rate para 9600

![1](../../en/01-arduino/img/1.png)

2. Abra o Assistente de Depuração Serial

[Serial Debug Assistant uartassist5.15.zip](https://juxitech.feishu.cn/wiki/BJlfwSQydi7u5lkRDQ6cV4dvnBd)

Selecione o número da porta serial

Defina o baud rate para `9600`

Bits de dados `8`, bits de parada `1`, paridade `NONE`, controle de fluxo `NONE`

Nas configurações de recebimento e envio, selecione `ASCII`

![2](../../en/01-arduino/img/2.png)

### 4. Descrição da API

| Função | Descrição |
|----------|-------------|
| `begin()` | Inicializa o sensor, retorna true/false |
| `getHeartbeatSPO2()` | Lê os dados de frequência cardíaca e SPO2, armazenados na struct `_sHeartbeatSPO2` |
| `getTemperature_C()` | Lê a temperatura a bordo (Celsius) |
| `sensorStartCollect()` | Inicia a coleta de dados (o LED do sensor acende) |
| `sensorEndCollect()` | Para a coleta de dados (o LED do sensor apaga) |

### 5. Descrição dos Dados

- **SPO2 (Saturação de Oxigênio no Sangue)**: Faixa normal 95% - 100%, valor -1 indica inválido
- **Heartbeat (Frequência Cardíaca)**: Faixa normal 60 - 100 BPM, valor -1 indica inválido
- **Motivos de Valores Inválidos**: Dedo não posicionado corretamente ou dados ainda não estabilizados

---

## Observações de Uso

### Dicas de Medição

1. **Posicionamento Correto do Dedo**
   - Posicione o dedo suavemente sobre o sensor, cobrindo os dois LEDs
   - Não pressione com força para não afetar a circulação sanguínea
   - Mantenha o dedo firme, sem se mover

2. **Aguarde a Estabilização dos Dados**
   - Os valores podem ficar instáveis no início da medição
   - Recomenda-se aguardar 10-30 segundos para os dados estabilizarem antes de fazer a leitura
   - O sensor atualiza os dados a cada 4 segundos

3. **Requisitos de Ambiente**
   - Evite luz forte incidindo diretamente sobre o sensor
   - Mantenha a temperatura do ambiente adequada
   - Fique quieto durante a medição

### Interpretação dos Dados

| Faixa de SPO2 | Descrição |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Hipóxia leve |
| < 90% | Hipóxia, recomenda-se consultar um médico |

| Faixa de Frequência Cardíaca | Descrição |
|-----------------|-------------|
| 60 - 100 BPM | Faixa normal para adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

---

## Perguntas Frequentes (FAQ)

### Q1: A inicialização do sensor falhou?

**R:**
1. Verifique se a fiação está correta (SDA para GPIO2/A4, SCL para GPIO3/A5)
2. Confirme se a alimentação está normal (3.3V ou 5V)
3. Use o comando `i2cdetect -y 1` para detectar o dispositivo
4. Certifique-se de que a chave DIP do sensor está na posição IIC

### Q2: Os dados sempre mostram -1?

**R:**
1. Confirme se o dedo está posicionado corretamente sobre o sensor
2. Aguarde alguns segundos para os dados estabilizarem
3. Verifique se `sensorStartCollect()` foi chamado para iniciar a coleta
4. Confirme se a luz indicadora do sensor está acesa

### Q3: Os dados estão imprecisos?

**R:**
1. Garanta que o dedo cobre totalmente a área óptica do sensor
2. Mantenha o dedo firme, sem se mover
3. Aguarde mais de 30 segundos para os dados estabilizarem
4. Faça várias medições e tire a média

### Q4: Quais placas de desenvolvimento Arduino são suportadas?

**R:** Suportadas:
- Arduino Uno/Nano/Mega
- ESP8266
- ESP32
- Outras placas de desenvolvimento compatíveis com o ambiente Arduino

---

## Localização dos Arquivos de Exemplo

### Exemplos Arduino
```
JUXI_HeartRate_SPO2/
└── examples/
    └── gainHeartbeatSPO2/
        └── gainHeartbeatSPO2.ino
```

