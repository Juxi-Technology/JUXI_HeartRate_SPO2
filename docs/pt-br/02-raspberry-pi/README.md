[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | Português (BR) | [Português (PT)](../../pt-pt/02-raspberry-pi/README.md) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# Tutorial Raspberry Pi JUXI_HeartRate_SPO2


## Índice

1. [Introdução](#introdução)
2. [Requisitos de Hardware](#requisitos-de-hardware)
3. [Conexões de Hardware](#conexões-de-hardware)
4. [Configuração do Ambiente](#configuração-do-ambiente)
5. [Uso do Código de Exemplo](#uso-do-código-de-exemplo)
6. [Referência da API](#referência-da-api)
7. [Perguntas Frequentes (FAQ)](#perguntas-frequentes-faq)
8. [Observações Importantes](#observações-importantes)

---

## Introdução

JUXI_HeartRate_SPO2 é um módulo sensor de frequência cardíaca e oxigenação do sangue baseado no chip MAX30102. Possui algoritmos embarcados que fornecem diretamente os valores de frequência cardíaca e saturação de oxigênio no sangue.

**Principais Características:**
- Medição da Saturação de Oxigênio no Sangue (SPO2)
- Medição da Frequência Cardíaca (batimentos por minuto)
- Medição de Temperatura a Bordo
- Suporte às comunicações UART e I2C

---

## Requisitos de Hardware

| Item Necessário | Descrição |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Recomenda-se Raspberry Pi 3B+ ou 4B |
| Sensor JUXI_HeartRate_SPO2 | Módulo sensor de frequência cardíaca e oxigenação do sangue |
| Fios Dupont | 4 jumpers fêmea-fêmea |
| Fonte de Alimentação | Fonte de alimentação para Raspberry Pi |

---

## Conexões de Hardware

### Método 1: Comunicação I2C (Recomendado)

A comunicação I2C tem fiação simples e é a recomendada.

| Pino do Sensor | Pino Físico da Raspberry Pi | Número BCM | Descrição |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 ou 17 | - | Alimentação 3.3V (5V também é aceitável) |
| GND | 6 ou 9 ou 14 | - | Terra (GND) |
| SDA | 3 | GPIO2 | Linha de Dados I2C |
| SCL | 5 | GPIO3 | Linha de Clock I2C |

**Importante:** Mude a chave do sensor para a posição **IIC**!

### Método 2: Comunicação Serial UART

A comunicação UART requer conexão cruzada.

| Pino do Sensor | Pino Físico da Raspberry Pi | Número BCM | Descrição |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 ou 4 | - | Alimentação 5V (3.3V também é aceitável) |
| GND | 6 ou 9 ou 14 | - | Terra (GND) |
| RX | 8 | GPIO14 | O RX do sensor conecta ao TX da Raspberry Pi |
| TX | 10 | GPIO15 | O TX do sensor conecta ao RX da Raspberry Pi |

**Importante:** Mude a chave do sensor para a posição **UART**!

![Diagrama de pinos da Raspberry Pi](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Configuração do Ambiente

### 1. Habilitar o I2C (Necessário para o Modo I2C)

```bash
sudo raspi-config
```

Selecione `Interface Options` → `I2C` → Selecione `Yes` para habilitar

Reinicie a Raspberry Pi:
```bash
sudo reboot
```

### 2. Habilitar a Porta Serial (Necessário para o Modo UART)

```bash
sudo raspi-config
```

Selecione `Interface Options` → `Serial`

- Primeira pergunta: "Would you like a login shell to be accessible over serial?" → Selecione `No`
- Segunda pergunta: "Would you like the serial port hardware to be enabled?" → Selecione `Yes`

Reinicie a Raspberry Pi:
```bash
sudo reboot
```

### 3. Instalar as Dependências

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Observação:** O modo I2C requer o `smbus2` — o pacote legado `python-smbus` não é suficiente.
> A biblioteca usa `smbus2.i2c_msg` para realizar duas transações I2C independentes (escrever o
> endereço de registro com STOP, depois uma nova transação de leitura para ler vários bytes
> em sequência), seguindo o timing de I2C exigido pelo chip do sensor.

### 4. Verificar a Conexão I2C (Modo I2C)

Depois de fazer a fiação, execute o comando abaixo para detectar dispositivos I2C:

```bash
i2cdetect -y 1
```

Se você vir o endereço `0x57`, o sensor foi conectado com sucesso.

---

## Uso do Código de Exemplo

### Estrutura de Arquivos

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Executando o Exemplo do Modo I2C

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Executando o Exemplo do Modo UART

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Observação:** É necessária permissão `sudo` para acessar a porta serial de hardware.

### Saída Esperada

Se tudo funcionar corretamente, você verá uma saída semelhante a:

```
==================================================
JUXI Heart Rate & Blood Oxygen Sensor - I2C Mode
==================================================

Initializing I2C bus 1, address 0x57...
Sensor initialized successfully!

Starting data collection...
Sensor LED is now ON!

Please place your finger on the sensor...

----------------------------------------
SPO2: 98 %
Heart Rate: 72 Times/min
Onboard Temperature: 25.5 °C
----------------------------------------
...
```

Pressione `Ctrl+C` para encerrar o programa.

---

## Referência da API

### Classe: JUXI_HeartRate_SPO2_i2c

Classe de sensor para comunicação I2C.

#### Construtor
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parâmetros:
- `bus_number`: Número do barramento I2C, geralmente 1 na Raspberry Pi
- `i2c_address`: Endereço I2C do sensor, padrão 0x57

#### Métodos

| Método | Descrição | Valor de Retorno |
|--------|-------------|--------------|
| `begin()` | Inicializa o sensor, verifica a conexão | bool (True em caso de sucesso) |
| `sensor_start_collect()` | Inicia a coleta de dados (LED do sensor LIGADO) | None |
| `sensor_end_collect()` | Para a coleta de dados (LED do sensor DESLIGADO) | None |
| `get_heartbeat_SPO2()` | Lê os dados de frequência cardíaca e SPO2 | None (resultados armazenados nas propriedades do objeto) |
| `get_temperature_c()` | Lê a temperatura a bordo | float (Celsius) |
| `close()` | Fecha a conexão I2C | None |

#### Propriedades

| Propriedade | Descrição |
|----------|-------------|
| `SPO2` | Saturação de Oxigênio no Sangue (%), -1 para valor inválido |
| `heartbeat` | Frequência Cardíaca (batimentos por minuto), -1 para valor inválido |

---

### Classe: JUXI_HeartRate_SPO2_uart

Classe de sensor para comunicação serial UART.

#### Construtor
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parâmetros:
- `port`: Caminho do dispositivo serial, padrão `/dev/serial0` na Raspberry Pi
- `baudrate`: Taxa de transmissão (baud rate), padrão 9600

#### Métodos

O mesmo que `JUXI_HeartRate_SPO2_i2c`.

---

## Perguntas Frequentes (FAQ)

### Q1: O que devo fazer se a inicialização do sensor falhar?

**R:** Siga estes passos:

1. **Verifique a Fiação**
   - Modo I2C: Confirme que o SDA conecta ao GPIO2 e o SCL ao GPIO3
   - Modo UART: Confirme a conexão cruzada RX-TX

2. **Verifique a Chave do Sensor**
   - Modo I2C: A chave deve estar na posição IIC
   - Modo UART: A chave deve estar na posição UART

3. **Verifique a Alimentação**
   - Confirme que o VCC conecta a 3.3V ou 5V
   - Confirme que o GND está conectado

4. **Verifique as Configurações do Sistema**
   - Modo I2C: Confirme que o I2C está habilitado
   - Modo UART: Confirme que a porta serial está habilitada

5. **Use os Comandos de Detecção**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### Q2: Os dados sempre mostram -1, o que devo fazer?

**R:**

1. Certifique-se de que o dedo está posicionado corretamente sobre o sensor, cobrindo totalmente os dois LEDs
2. Aguarde alguns segundos para os dados estabilizarem (geralmente 10-30 segundos)
3. Verifique se `sensor_start_collect()` foi chamado para iniciar a coleta
4. Verifique se o LED do sensor está aceso

### Q3: Os dados estão imprecisos, o que devo fazer?

**R:**

1. Garanta que o dedo cobre totalmente a área óptica do sensor
2. Mantenha o dedo firme, não se mova
3. Aguarde mais de 30 segundos para os dados estabilizarem
4. Faça várias medições e tire a média
5. Evite luz forte incidindo diretamente sobre o sensor

### Q4: Posso usar I2C e UART ao mesmo tempo?

**R:** Não, só é possível selecionar um método de comunicação por vez.

### Q5: Preciso usar sudo para executar?

**R:**
- Modo I2C: recomenda-se sudo para evitar problemas de permissão
- Modo UART: o sudo é obrigatório, caso contrário você não conseguirá acessar a porta serial

---

## Observações Importantes

### Dicas de Medição

1. **Posicionamento Correto do Dedo**
   - Posicione o dedo suavemente sobre o sensor, cobrindo os dois LEDs
   - Não pressione com muita força, pois isso pode afetar a circulação sanguínea
   - Mantenha o dedo firme, não se mova

2. **Aguarde a Estabilização dos Dados**
   - Os valores podem ficar instáveis no início da medição
   - Recomenda-se aguardar 10-30 segundos para os dados estabilizarem
   - O sensor atualiza os dados a cada 4 segundos

3. **Requisitos de Ambiente**
   - Evite luz forte incidindo diretamente sobre o sensor
   - Mantenha a temperatura ambiente adequada
   - Fique quieto durante a medição

### Interpretação dos Dados

| Faixa de SPO2 | Descrição |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Hipóxia leve |
| < 90% | Hipóxia, consulte um médico |

| Faixa de Frequência Cardíaca | Descrição |
|-----------------|-------------|
| 60 - 100 BPM | Faixa normal para adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

### Aviso de Segurança

- Este sensor é apenas para referência e não substitui equipamentos médicos profissionais
- Se você tiver preocupações de saúde, consulte um médico imediatamente
- Os resultados das medições são apenas para referência e não devem ser usados para diagnóstico

