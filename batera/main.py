import cv2
import numpy as np
import math
import pygame
import threading
import time


# Lista de círculos na ordem que devem ser tocados
circulos = [
    {"pos": (781, 615), "raio": 50, "encostou": False,"som":"caixa"},
    {"pos": (950, 475), "raio": 50, "encostou": False,"som":"ximbau"},
    {"pos": (780, 335), "raio": 50, "encostou": False,"som":"tom1"},
    {"pos": (580, 335), "raio": 50, "encostou": False,"som":"prato"},
    {"pos": (469, 535), "raio": 50, "encostou": False,"som":"surdo"}
]

# Inicializa o mixer
pygame.mixer.init()

# Carrega os sons
sons = {
    "caixa": pygame.mixer.Sound("sons/caixa.wav"),
    "ximbau": pygame.mixer.Sound("sons/ximbau.wav"),
    "tom1": pygame.mixer.Sound("sons/tom1.wav"),
    "prato": pygame.mixer.Sound("sons/prato.wav"),
    "surdo": pygame.mixer.Sound("sons/surdo.wav")
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


    cv2.circle(frame, (781, 615), 50, (0, 255, 0), 2) # -> caixa
    cv2.circle(frame, (950, 475), 50, (0, 255, 0), 2) # -> ximbau
    cv2.circle(frame, (780, 335), 50, (0, 255, 0), 2) # -> tom 1
    cv2.circle(frame, (580, 335), 50, (0, 255, 0), 2) # -> prato
    cv2.circle(frame, (469, 535), 50, (0, 255, 0), 2) # -> surdo


    
    cv2.imshow("Rastreamento dos baquetas", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
