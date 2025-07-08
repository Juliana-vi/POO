import random

class Bingo:
    def __init__(self, numBolas):
        self.numBolas = numBolas
        self.bolas_disponiveis = list(range(1, numBolas + 1))
        self.bolas_sorteadas = []

    def Sortear(self):
        if not self.bolas_disponiveis:
            return -1
        bola = random.choice(self.bolas_disponiveis)
        self.bolas_disponiveis.remove(bola)
        self.bolas_sorteadas.append(bola)
        return bola

    def Sorteados(self):
        return self.bolas_sorteadas.copy()


class BingoUI:
    @staticmethod
    def Menu():
        print("\n--- MENU BINGO ---")
        print("1. Iniciar novo jogo")
        print("2. Sortear número")
        print("3. Ver números sorteados")
        print("4. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def IniciarJogo():
        while True:
            try:
                n = int(input("Digite o número de bolas do bingo: "))
                if n > 0:
                    return Bingo(n)
                else:
                    print("Digite um número positivo.")
            except ValueError:
                print("Digite um número inteiro válido.")

    @staticmethod
    def Sortear(b):
        if b is None:
            raise ValueError("Nenhum jogo iniciado. Inicie um jogo antes de sortear.")
        bola = b.Sortear()
        if bola == -1:
            print("Todas as bolas já foram sorteadas")
        else:
            print(f"Bola sorteada: {bola}")

    @staticmethod
    def Sorteados(b):
        if b is None:
            print("Nenhum jogo iniciado.")
            return
        sorteados = b.Sorteados()
        if sorteados:
            print("Números sorteados:", sorted(sorteados))
        else:
            print("Nenhum número foi sorteado ainda.")

    @staticmethod
    def Main():
        bingo = None
        while True:
            opcao = BingoUI.Menu()
            if opcao == 1:
                bingo = BingoUI.IniciarJogo()
                print("Novo jogo iniciado")
            elif opcao == 2:
                BingoUI.Sortear(bingo)
            elif opcao == 3:
                BingoUI.Sorteados(bingo)
            elif opcao == 4:
                print("Saindo do jogo")
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    BingoUI.Main()