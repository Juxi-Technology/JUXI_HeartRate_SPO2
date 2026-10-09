[English](../../en/02-raspberry-pi/README.md) | [Deutsch](../../de/02-raspberry-pi/README.md) | [Español](../../es/02-raspberry-pi/README.md) | [Français](../../fr/02-raspberry-pi/README.md) | [Italiano](../../it/02-raspberry-pi/README.md) | [日本語](../../ja/02-raspberry-pi/README.md) | [한국어](../../ko/02-raspberry-pi/README.md) | [Português (BR)](../../pt-br/02-raspberry-pi/README.md) | Português (PT) | [简体中文](../../zh-hans/02-raspberry-pi/README.md) | [繁體中文](../../zh-hant/02-raspberry-pi/README.md)

# Tutorial do JUXI_HeartRate_SPO2 para Raspberry Pi


## Índice

1. [Introdução](#introdução)
2. [Requisitos de hardware](#requisitos-de-hardware)
3. [Ligações de hardware](#ligações-de-hardware)
4. [Configuração do ambiente](#configuração-do-ambiente)
5. [Utilização do código de exemplo](#utilização-do-código-de-exemplo)
6. [Referência da API](#referência-da-api)
7. [Perguntas frequentes](#perguntas-frequentes)
8. [Notas importantes](#notas-importantes)

---

## Introdução

JUXI_HeartRate_SPO2 é um módulo sensor de ritmo cardíaco e oxigénio no sangue baseado no chip MAX30102. Tem algoritmos incorporados que emitem diretamente os valores de ritmo cardíaco e de saturação de oxigénio no sangue.

**Principais características:**
- Medição da saturação de oxigénio no sangue (SPO2)
- Medição do ritmo cardíaco (batimentos por minuto)
- Medição de temperatura incorporada
- Suporte de comunicação UART e I2C

---

## Requisitos de hardware

| Item necessário | Descrição |
|--------------|-------------|
| Raspberry Pi (2/3/4/Zero) | Raspberry Pi 3B+ ou 4B recomendado |
| Sensor JUXI_HeartRate_SPO2 | Módulo sensor de ritmo cardíaco e oxigénio no sangue |
| Fios dupont | 4 fios jumper fêmea-fêmea |
| Adaptador de alimentação | Fonte de alimentação do Raspberry Pi |

---

## Ligações de hardware

### Método 1: comunicação I2C (recomendado)

A comunicação I2C tem uma ligação simples e é a recomendada.

| Pino do sensor | Pino físico do Raspberry Pi | Número BCM | Descrição |
|-----------|--------------------------|-----------|-------------|
| VCC | 1 ou 17 | - | Alimentação 3.3V (5V também aceitável) |
| GND | 6 ou 9 ou 14 | - | Massa |
| SDA | 3 | GPIO2 | Linha de dados I2C |
| SCL | 5 | GPIO3 | Linha de relógio I2C |

**Importante:** coloque o interruptor do sensor na posição **IIC**!

### Método 2: comunicação série UART

A comunicação UART exige ligação cruzada.

| Pino do sensor | Pino físico do Raspberry Pi | Número BCM | Descrição |
|-----------|--------------------------|-----------|-------------|
| VCC | 2 ou 4 | - | Alimentação 5V (3.3V também aceitável) |
| GND | 6 ou 9 ou 14 | - | Massa |
| RX | 8 | GPIO14 | O RX do sensor liga ao TX do Raspberry Pi |
| TX | 10 | GPIO15 | O TX do sensor liga ao RX do Raspberry Pi |

**Importante:** coloque o interruptor do sensor na posição **UART**!

![Diagrama de pinos do Raspberry Pi](../../en/02-raspberry-pi/Raspberry%20Pi%20Pin%20Diagram.png)

---

## Configuração do ambiente

### 1. Ativar o I2C (necessário para o modo I2C)

```bash
sudo raspi-config
```

Selecione `Interface Options` → `I2C` → selecione `Yes` para ativar

Reinicie o Raspberry Pi:
```bash
sudo reboot
```

### 2. Ativar a porta série (necessário para o modo UART)

```bash
sudo raspi-config
```

Selecione `Interface Options` → `Serial`

- Primeira pergunta: "Deseja que uma shell de início de sessão fique acessível através da porta série?" → selecione `No`
- Segunda pergunta: "Deseja que o hardware da porta série seja ativado?" → selecione `Yes`

Reinicie o Raspberry Pi:
```bash
sudo reboot
```

### 3. Instalar as dependências

```bash
# Update package lists
sudo apt-get update

# Install I2C tools and smbus2 library (smbus2 is required for I2C mode)
sudo apt-get install -y i2c-tools python3-smbus2

# Install pyserial (for serial port support)
sudo pip3 install pyserial
```

> **Nota:** o modo I2C requer o `smbus2` — o pacote legado `python-smbus` não é suficiente.
> A biblioteca utiliza `smbus2.i2c_msg` para efetuar duas transações I2C independentes (escrever o
> endereço do registo com STOP e, de seguida, uma nova transação de leitura para ler vários bytes
> sequencialmente), correspondendo à temporização I2C exigida pelo chip do sensor.

### 4. Verificar a ligação I2C (modo I2C)

Após a ligação, execute o seguinte comando para detetar os dispositivos I2C:

```bash
i2cdetect -y 1
```

Se vir o endereço `0x57`, o sensor está ligado com êxito.

---

## Utilização do código de exemplo

### Estrutura de ficheiros

```
python/raspberry/
├── JUXI_HeartRate_SPO2.py      # Main library file
└── examples/
    ├── i2c_example.py          # I2C mode example
    └── uart_example.py         # UART mode example
```

### Executar o exemplo do modo I2C

```bash
cd python/raspberry/examples
sudo python3 i2c_example.py
```

### Executar o exemplo do modo UART

```bash
cd python/raspberry/examples
sudo python3 uart_example.py
```

**Nota:** é necessária permissão `sudo` para aceder à porta série de hardware.

### Saída esperada

Se tudo funcionar corretamente, verá uma saída semelhante a:

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

Prima `Ctrl+C` para parar o programa.

---

## Referência da API

### Classe: JUXI_HeartRate_SPO2_i2c

Classe do sensor para comunicação I2C.

#### Construtor
```python
JUXI_HeartRate_SPO2_i2c(bus_number=1, i2c_address=0x57)
```

Parâmetros:
- `bus_number`: número do barramento I2C, normalmente 1 no Raspberry Pi
- `i2c_address`: endereço I2C do sensor, predefinido 0x57

#### Métodos

| Método | Descrição | Valor devolvido |
|--------|-------------|--------------|
| `begin()` | Inicializa o sensor e verifica a ligação | bool (True em caso de êxito) |
| `sensor_start_collect()` | Inicia a recolha de dados (LED do sensor ligado) | None |
| `sensor_end_collect()` | Para a recolha de dados (LED do sensor desligado) | None |
| `get_heartbeat_SPO2()` | Lê os dados de ritmo cardíaco e SPO2 | None (resultados armazenados nas propriedades do objeto) |
| `get_temperature_c()` | Lê a temperatura incorporada | float (Celsius) |
| `close()` | Fecha a ligação I2C | None |

#### Propriedades

| Propriedade | Descrição |
|----------|-------------|
| `SPO2` | Saturação de oxigénio no sangue (%), -1 para valor inválido |
| `heartbeat` | Ritmo cardíaco (batimentos por minuto), -1 para valor inválido |

---

### Classe: JUXI_HeartRate_SPO2_uart

Classe do sensor para comunicação série UART.

#### Construtor
```python
JUXI_HeartRate_SPO2_uart(port='/dev/serial0', baudrate=9600)
```

Parâmetros:
- `port`: caminho do dispositivo série, predefinido `/dev/serial0` no Raspberry Pi
- `baudrate`: taxa de baud, predefinida 9600

#### Métodos

O mesmo que `JUXI_HeartRate_SPO2_i2c`.

---

## Perguntas frequentes

### P1: O que devo fazer se a inicialização do sensor falhar?

**R:** Siga estes passos:

1. **Verifique a ligação**
   - Modo I2C: verifique se o SDA liga ao GPIO2 e o SCL ao GPIO3
   - Modo UART: verifique a ligação cruzada RX-TX

2. **Verifique o interruptor do sensor**
   - Modo I2C: o interruptor deve estar na posição IIC
   - Modo UART: o interruptor deve estar na posição UART

3. **Verifique a alimentação**
   - Verifique se o VCC liga a 3.3V ou 5V
   - Verifique se o GND está ligado

4. **Verifique as definições do sistema**
   - Modo I2C: verifique se o I2C está ativado
   - Modo UART: verifique se a porta série está ativada

5. **Utilize comandos de deteção**
   ```bash
   # I2C mode
   i2cdetect -y 1
   
   # UART mode
   ls /dev/serial*
   ```

### P2: Os dados mostram sempre -1, o que devo fazer?

**R:**

1. Certifique-se de que o dedo está bem colocado sobre o sensor, cobrindo totalmente os dois LEDs
2. Aguarde alguns segundos até os dados estabilizarem (normalmente 10-30 segundos)
3. Verifique se `sensor_start_collect()` foi chamado para iniciar a recolha
4. Verifique se o LED do sensor está aceso

### P3: Os dados estão imprecisos, o que devo fazer?

**R:**

1. Certifique-se de que o dedo cobre totalmente a zona ótica do sensor
2. Mantenha o dedo imóvel, não o mova
3. Aguarde mais de 30 segundos até os dados estabilizarem
4. Faça várias medições e calcule a média
5. Evite luz forte direta sobre o sensor

### P4: Posso utilizar I2C e UART ao mesmo tempo?

**R:** Não, só é possível selecionar um método de comunicação de cada vez.

### P5: Preciso de utilizar sudo para executar?

**R:**
- Modo I2C: recomenda-se o sudo para evitar problemas de permissões
- Modo UART: o sudo é obrigatório, caso contrário não consegue aceder à porta série

---

## Notas importantes

### Dicas de medição

1. **Posicionamento correto do dedo**
   - Coloque o dedo suavemente sobre o sensor, cobrindo os dois LEDs
   - Não pressione com demasiada força, pois pode afetar a circulação sanguínea
   - Mantenha o dedo estável, não o mova

2. **Aguarde a estabilização dos dados**
   - Os valores podem ficar instáveis ao iniciar a medição
   - Recomenda-se aguardar 10-30 segundos até os dados estabilizarem
   - O sensor atualiza os dados a cada 4 segundos

3. **Requisitos do ambiente**
   - Evite luz forte direta sobre o sensor
   - Mantenha uma temperatura ambiente adequada
   - Mantenha-se tranquilo durante a medição

### Interpretação dos dados

| Intervalo de SPO2 | Descrição |
|-----------|-------------|
| 95% - 100% | Normal |
| 90% - 94% | Hipóxia ligeira |
| < 90% | Hipóxia, consulte um médico |

| Intervalo de ritmo cardíaco | Descrição |
|-----------------|-------------|
| 60 - 100 BPM | Intervalo normal para adultos |
| < 60 BPM | Bradicardia |
| > 100 BPM | Taquicardia |

### Aviso de segurança

- Este sensor destina-se apenas a referência e não substitui equipamento médico profissional
- Se tiver preocupações de saúde, consulte um médico prontamente
- Os resultados das medições são apenas indicativos e não devem ser utilizados para diagnóstico
