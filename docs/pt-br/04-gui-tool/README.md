[English](../../en/04-gui-tool/README.md) | [Deutsch](../../de/04-gui-tool/README.md) | [Español](../../es/04-gui-tool/README.md) | [Français](../../fr/04-gui-tool/README.md) | [Italiano](../../it/04-gui-tool/README.md) | [日本語](../../ja/04-gui-tool/README.md) | [한국어](../../ko/04-gui-tool/README.md) | Português (BR) | [Português (PT)](../../pt-pt/04-gui-tool/README.md) | [简体中文](../../zh-hans/04-gui-tool/README.md) | [繁體中文](../../zh-hant/04-gui-tool/README.md)

# Módulo Oxímetro de Frequência Cardíaca - Guia do Usuário da GUI

## 📋 Recursos

Este é um programa gráfico de monitoramento de frequência cardíaca e oxigenação do sangue com os seguintes recursos:

1. ✅ **Seleção de Porta Serial** - Digitaliza automaticamente as portas seriais disponíveis
2. ✅ **Seleção de Baud Rate** - Suporta 9600/19200/38400/57600/115200
3. ✅ **Conectar/Desconectar** - Conexão/desconexão do módulo com um clique
4. ✅ **Iniciar/Parar Coleta** - Controla o LED do sensor (ligado/desligado)
5. ✅ **Iniciar/Parar Monitoramento** - Exibição de dados em tempo real
6. ✅ **Exibição de Dados em Tempo Real** - Oxigenação do sangue, frequência cardíaca, temperatura
7. ✅ **Alternância Inglês / Chinês** - Troque o idioma da interface a qualquer momento; o padrão é o inglês

---

## 🔌 Conexão de Hardware

| Módulo Oxímetro de Frequência Cardíaca | Módulo USB para TTL |
|---------------------------|------------------|
| **VCC** | **5V** (Importante! Não use 3.3V) |
| **GND** | **GND** |
| **TX** | **RX** (Conexão cruzada) |
| **RX** | **TX** (Conexão cruzada) |

⚠️ **Observação: TX e RX devem ser conectados de forma cruzada!**

---

## 🚀 Executando o Programa

### Método 1: Executar o Script Python Diretamente

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

## 📖 Passos de Uso

### Passo 1: Conectar o Hardware
1. Conecte o sensor e o USB para TTL de acordo com a tabela de fiação acima

   VCC -> VCC

   GND -> GND

   RX -> TX

   TX -> RX

2. Conecte o USB para TTL à porta USB do computador

### Passo 2: Abrir o Programa
Execute `HeartRateOximeter.exe`

### Passo 3: Configurações da Porta Serial
1. Selecione a porta serial correta (por exemplo, COM3)
2. Selecione o baud rate **9600** (padrão)
3. Clique no botão [Connect]

### Passo 4: Iniciar a Coleta
1. Após a conexão bem-sucedida, clique em [Start Collection]
2. ✅ O LED do sensor acenderá

### Passo 5: Iniciar o Monitoramento
1. Posicione o dedo sobre o sensor
2. Clique em [Start Monitoring]
3. Visualize os dados em tempo real

---

## 📊 Descrição da Interface

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

**Troca de idioma**: o menu suspenso no topo da janela alterna a interface entre inglês e chinês. O programa inicia em inglês.

---

## 📋 Interpretação dos Dados

| Dado | Faixa Normal | Descrição |
|------|-------------|-------------|
| **SPO2** | 95% - 100% | Consulte um médico se estiver abaixo de 90% |
| **Frequência Cardíaca** | 60 - 100 BPM | Faixa normal para adultos |
| **Temperatura** | 25 - 35 °C | Temperatura a bordo do módulo, não é a temperatura corporal |

**Observação**: Logo após iniciar, ou se o dedo não estiver posicionado corretamente, os dados podem mostrar -1, o que é normal.

---

## ❓ Perguntas Frequentes (FAQ)

### Q1: Não consigo encontrar a porta serial?
**R:**
1. Verifique se o driver do USB para TTL está instalado corretamente
2. Reconecte o cabo USB
3. Clique no botão [Refresh] para digitalizar novamente

### Q2: A conexão falhou?
**R:**
1. Confirme se a porta serial selecionada está correta
2. Confirme se a porta serial não está ocupada por outros programas (por exemplo, assistente serial, Arduino IDE)
3. Verifique se o módulo USB para TTL está funcionando corretamente

### Q3: O LED não acende após clicar em Start Collection?
**R:**
1. Verifique se o VCC está conectado a 5V (não 3.3V)
2. Verifique se o TX/RX estão conectados de forma cruzada
3. Confirme se o próprio módulo sensor não está danificado

### Q4: Os dados sempre mostram -1?
**R:**
1. Confirme se [Start Collection] foi clicado
2. Posicione o dedo corretamente sobre o sensor, cobrindo totalmente a área do LED
3. Mantenha o dedo firme e aguarde alguns segundos
4. Verifique se há conexões soltas

### Q5: O programa não responde?
**R:**
1. Clique primeiro em [Stop Monitoring]
2. Depois clique em [Stop Collection]
3. Por fim, clique em [Disconnect]
4. Reinicie o programa

---

## ⚠️ Cuidados

1. **Ordem de fiação**: Conecte o sensor primeiro e só depois conecte o USB
2. **Ordem de desconexão**: Pare o monitoramento, depois pare a coleta e, por fim, desconecte
3. **Requisito de alimentação**: O sensor deve ser conectado à alimentação de 5V; 3.3V pode não funcionar corretamente
4. **Posicionamento do dedo**: O dedo deve cobrir totalmente a área óptica, não pressione com força
5. **Requisito de ambiente**: Evite luz forte incidindo diretamente sobre o sensor

---

## 📞 Suporte Técnico

Se você encontrar problemas, verifique:
1. Fiação de hardware correta (especialmente o cruzamento TX/RX)
2. A fonte de alimentação é 5V
3. O driver do USB para TTL está funcionando corretamente
4. A porta serial não está ocupada por outros programas
