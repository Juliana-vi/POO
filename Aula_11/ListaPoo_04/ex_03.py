class Pais:
    def __init__(self, i: int, n: str, p: int, a: float):
        self.id = i
        self.nome = n
        self.populacao = p
        self.area = a

    def Densidade(self) -> float:
        if self.area == 0:
            return 0
        return self.populacao / self.area

    def ToString(self) -> str:
        return f"ID: {self.id} | Nome: {self.nome} | População: {self.populacao} | Área: {self.area:.2f} km² | Densidade: {self.Densidade():.2f} hab/km²"


class PaisUI:
    __paises = []

    @staticmethod
    def Menu():
        print("\n--- Cadastro de Países ---")
        print("1. Inserir novo país")
        print("2. Listar países")
        print("3. Atualizar país")
        print("4. Excluir país")
        print("5. País mais populoso")
        print("6. País mais povoado")
        print("7. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def Inserir():
        try:
            i = int(input("ID: "))
            n = input("Nome: ")
            p = int(input("População: "))
            a = float(input("Área (km²): "))
            PaisUI.__paises.append(Pais(i, n, p, a))
            print("País inserido")
        except ValueError:
            print("Dados inválidos")

    @staticmethod
    def Listar():
        if not PaisUI.__paises:
            print("Nenhum país cadastrado")
        for pais in PaisUI.__paises:
            print(pais.ToString())

    @staticmethod
    def Atualizar():
        try:
            i = int(input("Informe o ID do país a ser atualizado: "))
            for pais in PaisUI.__paises:
                if pais.id == i:
                    n = input("Novo nome: ")
                    p = int(input("Nova população: "))
                    a = float(input("Nova área (km²): "))
                    pais.nome = n
                    pais.populacao = p
                    pais.area = a
                    print("País atualizado")
                    return
            print("País não encontrado")
        except ValueError:
            print("Dados inválidos")

    @staticmethod
    def Excluir():
        try:
            i = int(input("Informe o ID do país a ser excluído: "))
            for pais in PaisUI.__paises:
                if pais.id == i:
                    PaisUI.__paises.remove(pais)
                    print("País excluído")
                    return
            print("País não encontrado")
        except ValueError:
            print("ID inválido")

    @staticmethod
    def MaisPopuloso():
        if not PaisUI.__paises:
            print("Nenhum país cadastrado")
            return
        pais = max(PaisUI.__paises, key=lambda p: p.populacao)
        print("País mais populoso:")
        print(pais.ToString())

    @staticmethod
    def MaisPovoado():
        if not PaisUI.__paises:
            print("Nenhum país cadastrado")
            return
        pais = max(PaisUI.__paises, key=lambda p: p.Densidade())
        print("País mais povoado:")
        print(pais.ToString())

    @staticmethod
    def Main():
        while True:
            op = PaisUI.Menu()
            if op == 1:
                PaisUI.Inserir()
            elif op == 2:
                PaisUI.Listar()
            elif op == 3:
                PaisUI.Atualizar()
            elif op == 4:
                PaisUI.Excluir()
            elif op == 5:
                PaisUI.MaisPopuloso()
            elif op == 6:
                PaisUI.MaisPovoado()
            elif op == 7:
                print("Saindo do programa")
                break
            else:
                print("Opção inválida")

if __name__ == "__main__":
    PaisUI.Main()