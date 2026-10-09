[English](../../en/04-gui-tool/README.md) | [Deutsch](../../de/04-gui-tool/README.md) | [Español](../../es/04-gui-tool/README.md) | [Français](../../fr/04-gui-tool/README.md) | [Italiano](../../it/04-gui-tool/README.md) | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | [Português (BR)](../../pt-br/04-gui-tool/README.md) | Português (PT) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Módulo Oxímetro de Ritmo Cardíaco - Guia do utilizador da ferramenta gráfica

## 📋 Funcionalidades

Este é um programa gráfico de monitorização de ritmo cardíaco e oxigénio no sangue com as seguintes funcionalidades:

1. ✅ **Seleção da porta série** - Deteta automaticamente as portas série disponíveis
2. ✅ **Seleção da taxa de baud** - Suporta 9600/19200/38400/57600/115200
3. ✅ **Ligar/desligar** - Liga/desliga o módulo com um clique
4. ✅ **Iniciar/parar recolha** - Controla o acender/apagar do LED do sensor
5. ✅ **Iniciar/parar monitorização** - Apresentação de dados em tempo real
6. ✅ **Apresentação de dados em tempo real** - Oxigénio no sangue, ritmo cardíaco, temperatura
7. ✅ **Alternância entre inglês e chinês** - Muda o idioma da interface em qualquer momento; o inglês é o predefinido

---

## 🔌 Ligação do hardware

| Módulo oxímetro de ritmo cardíaco | Módulo USB para TTL |
|---------------------------|------------------|
| **VCC** | **5V** (Importante! Não utilize 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (ligação cruzada) |
| **RX** | **TX** (ligação cruzada) |

⚠️ **Nota: o TX e o RX têm de estar ligados de forma cruzada!**

---

## 🚀 Execução do programa

### Método 1: executar diretamente o script Python

1. Instale as dependências:
```bash
pip install pyserial
```

2. Execute o programa:
```bash
cd 上位机源代码
python HeartRateOximeter.py
```

---

## 📖 Passos de utilização

### Passo 1: ligar o hardware
1. Ligue o sensor e o módulo USB para TTL de acordo com a tabela de ligações acima

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Ligue o módulo USB para TTL a uma porta USB do computador

### Passo 2: abrir o programa
Execute `HeartRateOximeter.exe`

### Passo 3: configurações da porta série
1. Selecione a porta série correta (por exemplo, COM3)
2. Selecione a taxa de baud **9600** (predefinida)
3. Clique no botão [Connect]

### Passo 4: iniciar a recolha
1. Após a ligação com êxito, clique em [Start Collection]
2. ✅ O LED do sensor acende

### Passo 5: iniciar a monitorização
1. Coloque o dedo sobre o sensor
2. Clique em [Start Monitoring]
3. Consulte os dados em tempo real

---

## 📊 Descrição da interface

```
┌─────────────────────────────────────────┐
│  Language:               [English ↓]    │
├─────────────────────────────────────────┤
│         Serial Port Settings            │
│  Port:   [COM3  ↓]  [Refresh]          │
│  Baud:   [9600  ↓]  [Connect]          │
├─────────────────────────────────────────┤
│         Module Control                  │
│  [Start Collection]  [Start Monitoring] │
├─────────────────────────────────────────┤
│         Real-time Data                  │
│  SPO2:              98 %                │
│  Heart Rate:        75 BPM              │
│  Temperature:       36.6 °C             │
│  Status:  Monitoring...                 │
├─────────────────────────────────────────┤
│         Usage Tips                      │
│  1. Wiring: VCC->5V, GND->GND, RX->TX, TX->RX  │
│  2. Click Connect before starting collection     │
│  3. Sensor LED turns on after collection starts  │
└─────────────────────────────────────────┘
```

**Alternância de idioma**: o menu pendente no topo da janela alterna a interface entre inglês e 中文. O programa inicia em inglês.

---

## 📋 Interpretação dos dados

| Dados | Intervalo normal | Descrição |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Consulte um médico se for inferior a 90% |
| **Heart Rate** | 60 - 100 BPM | Intervalo normal para adultos |
| **Temperature** | 25 - 35 °C | Temperatura incorporada no módulo, não é a temperatura corporal |

**Nota**: Quando o programa acabou de arrancar ou o dedo não está bem colocado, os dados podem mostrar -1, o que é normal.

---

## ❓ Perguntas frequentes

### P1: Não encontra a porta série?
**R:**
1. Verifique se o controlador do módulo USB para TTL está instalado corretamente
2. Volte a ligar o cabo USB
3. Clique no botão [Refresh] para voltar a detetar

### P2: Falha na ligação?
**R:**
1. Confirme que selecionou a porta série correta
2. Confirme que a porta série não está ocupada por outros programas (por exemplo, assistente série, Arduino IDE)
3. Verifique se o módulo USB para TTL está a funcionar corretamente

### P3: O LED não acende depois de clicar em Start Collection?
**R:**
1. Verifique se o VCC está ligado a 5V (e não a 3.3V)
2. Verifique se o TX/RX estão ligados de forma cruzada
3. Confirme que o próprio módulo sensor não está danificado

### P4: Os dados mostram sempre -1?
**R:**
1. Confirme que [Start Collection] foi clicado
2. Coloque o dedo corretamente sobre o sensor, cobrindo totalmente a zona do LED
3. Mantenha o dedo estável e aguarde alguns segundos
4. Verifique se há ligações soltas

### P5: O programa não responde?
**R:**
1. Clique primeiro em [Stop Monitoring]
2. De seguida, clique em [Stop Collection]
3. Por fim, clique em [Disconnect]
4. Reinicie o programa

---

## ⚠️ Precauções

1. **Ordem de ligação**: ligue primeiro o sensor e só depois o USB
2. **Ordem de desligamento**: pare a monitorização, depois a recolha e, por fim, desligue
3. **Alimentação necessária**: o sensor tem de estar ligado a 5V; com 3.3V pode não funcionar corretamente
4. **Posicionamento do dedo**: o dedo deve cobrir totalmente a zona ótica; não pressione com força
5. **Condições do ambiente**: evite luz forte direta sobre o sensor

---

## 📞 Assistência técnica

Se encontrar problemas, verifique:
1. Se a ligação do hardware está correta (especialmente o cruzamento TX/RX)
2. Se a alimentação é de 5V
3. Se o controlador do módulo USB para TTL está a funcionar corretamente
4. Se a porta série não está ocupada por outros programas
