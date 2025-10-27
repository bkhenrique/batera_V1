# Bateria Virtual com OpenCV e Pygame

Este projeto permite tocar uma bateria virtual utilizando uma webcam.
A detecção é feita com OpenCV, rastreando objetos vermelhos (como pontas de baquetas marcadas com fita vermelha).
Quando o objeto encosta em uma das regiões definidas na tela, o programa toca o som correspondente (caixa, surdo, prato, etc.), usando Pygame.

## Funcionalidades

- Rastreamento em tempo real de objetos vermelhos via webcam
- Áudio responsivo ao toque nas áreas predefinidas (simulando partes de uma bateria)
- Sons independentes para cada peça da bateria
- Visualização na tela com círculos representando os tambores e pratos

## Tecnologias utilizadas

- Python 3.x
- OpenCV
- NumPy
- Pygame

## Estrutura do projeto

```
batera_V1/
│
├── batera/
│   ├── main.py
│   └── sons/
│       ├── caixa.wav
│       ├── ximbau.wav
│       ├── tom1.wav
│       ├── tom2.wav
│       ├── prato.wav
│       └── surdo.wav
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Interface Gráfica

SIM! Este projeto possui interface gráfica que mostra:
- Imagem da webcam em tempo real
- Círculos verdes representando as peças da bateria
- Rastreamento do objeto vermelho (baqueta)
- Coordenadas do objeto detectado

## Início Rápido (Mac)

Se você está no Mac e quer testar agora:

```bash
# 1. Instalar dependências
pip3 install -r requirements.txt

# 2. Executar
python3 batera/main.py
```

Pronto! A janela com a webcam deve abrir. Pressione ESC para sair.

## Instalação e execução

### IMPORTANTE: Escolha o método adequado para seu sistema

- **Mac e Windows**: Recomendado executar LOCALMENTE (sem Docker)
- **Linux**: Docker funciona perfeitamente

### Mac (Recomendado: Execução Local)

1. Instale o Python 3.11 ou superior:
```bash
brew install python@3.11
```

2. Instale as dependências:
```bash
pip3 install -r requirements.txt
```

3. Execute o programa:
```bash
python3 batera/main.py
```

#### Mac com Docker (Avançado - Não Recomendado)

O Docker no Mac tem limitações com webcam e GUI. Se ainda quiser tentar:

1. Instale o XQuartz:
```bash
brew install --cask xquartz
```

2. Abra o XQuartz e vá em Preferências > Segurança > Marque "Permitir conexões de clientes de rede"

3. Reinicie o Mac

4. No terminal:
```bash
xhost +localhost
export DISPLAY=:0
docker-compose up
```

Nota: A webcam pode não funcionar corretamente no Docker no Mac.

### Windows (Recomendado: Execução Local)

1. Instale o Python 3.11 ou superior do site oficial: https://www.python.org/downloads/

2. Abra o PowerShell ou CMD e instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python batera/main.py
```

#### Windows com Docker (Avançado - Não Recomendado)

Requer WSL2 e configuração complexa. Recomendamos executar localmente.

### Linux (Recomendado: Docker)

1. Permitir acesso ao display:
```bash
xhost +local:docker
```

2. Construir e executar:
```bash
docker-compose up
```

3. Para parar, pressione `ESC` na janela da aplicação ou `Ctrl+C` no terminal.

#### Linux - Execução Local (Alternativa)

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o programa:
```bash
python batera/main.py
```

## Como usar

1. Certifique-se de que sua webcam está ligada
2. Coloque uma fita vermelha na ponta de uma baqueta ou caneta
3. Mire na tela: você verá os círculos representando as partes da bateria
4. Quando o objeto vermelho encostar em um círculo, o som correspondente será reproduzido
5. Pressione ESC para encerrar o programa

## Mapeamento dos sons

| Posição (x, y) | Som     | Descrição              |
|----------------|---------|------------------------|
| (781, 615)     | caixa   | Caixa central          |
| (950, 475)     | ximbau  | Prato de condução      |
| (780, 335)     | tom1    | Tom pequeno            |
| (580, 335)     | prato   | Prato crash            |
| (469, 535)     | surdo   | Surdo ou bumbo lateral |

## Possíveis melhorias

- Implementar detecção de múltiplas cores (para rastrear as duas baquetas)
- Adicionar animações nas áreas tocadas
- Ajustar sensibilidade e ruído da câmera
- Tornar as posições dos círculos configuráveis
- Adicionar mais sons e peças de bateria

## Solução de problemas

### Docker: Webcam não detectada
Verifique se a webcam está em `/dev/video0`:
```bash
ls -l /dev/video*
```

### Docker: Sem áudio
Certifique-se de que o PulseAudio está rodando:
```bash
pulseaudio --check
```

### Docker: Erro de display
Verifique se executou `xhost +local:docker` antes de rodar o container.
