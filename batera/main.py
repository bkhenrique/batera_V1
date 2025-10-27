import cv2
import numpy as np
import math
import pygame
import threading
import time
import os
import json

# Obtém o diretório onde este arquivo está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONS_DIR = os.path.join(BASE_DIR, "sons")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Posições padrão
POSICOES_PADRAO = {
    "caixa": (781, 615),
    "ximbau": (950, 475),
    "tom1": (780, 335),
    "prato": (580, 335),
    "surdo": (469, 535)
}

# Carrega configuração se existir
def carregar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            print("Configuração carregada de:", CONFIG_FILE)
            posicoes = config.get("posicoes", POSICOES_PADRAO)
            # Converte listas para tuplas
            posicoes = {k: tuple(v) if isinstance(v, list) else v for k, v in posicoes.items()}
            return posicoes, config.get("espelhar", True)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            print("Usando posições padrão")
            return POSICOES_PADRAO, True
    return POSICOES_PADRAO, True

posicoes_config, ESPELHAR_CAMERA = carregar_config()

# Lista de círculos na ordem que devem ser tocados
circulos = [
    {"pos": posicoes_config["caixa"], "raio": 50, "encostou": False,"som":"caixa"},
    {"pos": posicoes_config["ximbau"], "raio": 50, "encostou": False,"som":"ximbau"},
    {"pos": posicoes_config["tom1"], "raio": 50, "encostou": False,"som":"tom1"},
    {"pos": posicoes_config["prato"], "raio": 50, "encostou": False,"som":"prato"},
    {"pos": posicoes_config["surdo"], "raio": 50, "encostou": False,"som":"surdo"}
]

# Inicializa o mixer
pygame.mixer.init()

# Carrega os sons usando caminhos absolutos
sons = {
    "caixa": pygame.mixer.Sound(os.path.join(SONS_DIR, "caixa.wav")),
    "ximbau": pygame.mixer.Sound(os.path.join(SONS_DIR, "ximbau.wav")),
    "tom1": pygame.mixer.Sound(os.path.join(SONS_DIR, "tom1.wav")),
    "prato": pygame.mixer.Sound(os.path.join(SONS_DIR, "prato.wav")),
    "surdo": pygame.mixer.Sound(os.path.join(SONS_DIR, "surdo.wav"))
}


#funcão para tocar o som ja carregado
def tocar(som):
    sons[som].play()
  

#define se a "baqueta" encostou no circulo
def encostou_no_circulo(x_obj, y_obj, circulo):
    x_c, y_c = circulo["pos"]
    raio = circulo["raio"]
    distancia = math.sqrt((x_obj - x_c)**2 + (y_obj - y_c)**2)
    return distancia <= raio



cap = cv2.VideoCapture(0)

# Faixas de vermelho
lower_red1 = np.array([0, 130, 120])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 130, 120])
upper_red2 = np.array([180, 255, 255])



while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Espelha a câmera (como um espelho)
    if ESPELHAR_CAMERA:
        frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    for c in contours:
        area = cv2.contourArea(c)
        if area > 800:  # ignora pequenos ruídos
            (x, y), radius = cv2.minEnclosingCircle(c)
            if radius > 5:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.putText(frame, f"({int(x)}, {int(y)})", (int(x)-40, int(y)-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                for i, circulo in enumerate(circulos):
                    if encostou_no_circulo(x, y, circulo):
                        if not circulo["encostou"]:  # evita múltiplos prints para o mesmo círculo
                            tocar(circulo["som"])
                            circulo["encostou"] = True
                            print("encostou")
                    else:
                        circulo["encostou"] = False  # permite detectar novamente se o objeto sair e voltar


    # Desenha os círculos nas posições calibradas
    for circulo in circulos:
        x, y = circulo["pos"]
        cv2.circle(frame, (int(x), int(y)), circulo["raio"], (0, 255, 0), 2)


    
    cv2.imshow("Rastreamento dos baquetas", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
