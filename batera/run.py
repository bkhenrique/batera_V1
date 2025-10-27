#!/usr/bin/env python3
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("\n=== BATERIA VIRTUAL ===\n")
    print("1. Calibrar posições dos círculos")
    print("2. Rodar bateria")
    print("3. Sair\n")
    
    opcao = input("Escolha uma opção (1-3): ").strip()
    
    if opcao == "1":
        print("\nAbrindo modo de calibração...")
        print("Clique nos círculos na ordem indicada.\n")
        from calibrate import calibrar
        calibrar()
    elif opcao == "2":
        print("\nRodando bateria virtual...")
        print("Pressione ESC para sair.\n")
        import main
    elif opcao == "3":
        print("Saindo...")
        sys.exit(0)
    else:
        print("Opção inválida!")
        main()

if __name__ == "__main__":
    main()

