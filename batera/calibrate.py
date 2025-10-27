import cv2
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Posições padrão
DEFAULT_POSITIONS = {
    "caixa": (781, 615),
    "ximbau": (950, 475),
    "tom1": (780, 335),
    "prato": (580, 335),
    "surdo": (469, 535)
}

# Ordem dos sons para calibração
ORDEM_CALIBRACAO = ["caixa", "ximbau", "tom1", "prato", "surdo"]

# Variáveis globais
posicoes = DEFAULT_POSITIONS.copy()
indice_atual = 0
frame_atual = None
mouse_x = 0
mouse_y = 0

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, indice_atual
    
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y
        som_atual = ORDEM_CALIBRACAO[indice_atual]
        posicoes[som_atual] = (x, y)
        print(f"Posição de '{som_atual}' definida para: ({x}, {y})")
        indice_atual += 1

def calibrar():
    global frame_atual
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Não consegui abrir a câmera!")
        return
    
    cv2.namedWindow("Calibração - Clique nos círculos")
    cv2.setMouseCallback("Calibração - Clique nos círculos", mouse_callback)
    
    print("\n=== MODO DE CALIBRAÇÃO ===")
    print("Clique nos círculos na seguinte ordem:")
    for i, som in enumerate(ORDEM_CALIBRACAO, 1):
        print(f"{i}. {som.upper()}")
    print("\nPressione ESC para sair\n")
    
    while indice_atual < len(ORDEM_CALIBRACAO):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Espelha a câmera (como um espelho)
        frame = cv2.flip(frame, 1)
        frame_atual = frame.copy()
        
        # Desenha os círculos já calibrados
        for i, som in enumerate(ORDEM_CALIBRACAO):
            if i < indice_atual:
                x, y = posicoes[som]
                cv2.circle(frame, (x, y), 50, (0, 255, 0), 2)
                cv2.putText(frame, som, (x - 30, y - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            elif i == indice_atual:
                # Círculo em amarelo para o próximo a calibrar
                x, y = posicoes[som]
                cv2.circle(frame, (x, y), 50, (0, 255, 255), 3)
                cv2.putText(frame, f"CLIQUE AQUI: {som.upper()}", (x - 100, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Mostra instruções
        cv2.putText(frame, f"Calibrando: {ORDEM_CALIBRACAO[indice_atual].upper()} ({indice_atual + 1}/{len(ORDEM_CALIBRACAO)})", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Pressione ESC para sair", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        cv2.imshow("Calibração - Clique nos círculos", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if indice_atual == len(ORDEM_CALIBRACAO):
        salvar_configuracao()
        print("\nCalibração concluída com sucesso!")
        print(f"Posições salvas em: {CONFIG_FILE}")
    else:
        print("\nCalibração cancelada!")

def salvar_configuracao():
    config = {
        "posicoes": posicoes,
        "espelhar": True
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuração salva: {json.dumps(config, indent=2)}")

def carregar_configuracao():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            return config
        except:
            return None
    return None

if __name__ == "__main__":
    calibrar()

