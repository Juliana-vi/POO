from datetime import datetime

class Treino:
    def __init__(self, id: int, data: datetime, distancia: float, tempo: datetime):
        self._id = id
        self._data = data
        self._distancia = distancia
        self._tempo = tempo

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data

    def get_distancia(self):
        return self._distancia

    def get_tempo(self):
        return self._tempo

    def set_data(self, data):
        self._data = data

    def set_distancia(self, distancia):
        self._distancia = distancia

    def set_tempo(self, tempo):
        self._tempo = tempo

    def ToString(self):
        return (f"ID: {self._id}\n"
                f"Data do treino: {self._data}\n"
                f"Distância percorrida: {self._distancia}\n"
                f"Tempo da corrida: {self._tempo}\n"

class TreinoUI:
    treinos = []

    @staticmethod
    def Main():
        while True:
            opcao = TreinoUI.Menu()
            if opcao == 1:
                TreinoUI.Inserir()
            elif opcao == 2:
                TreinoUI.Listar()
            elif opcao == 3:
                TreinoUI.Listar_id()
            elif opcao == 4:
                TreinoUI.Atualizar()
            elif opcao == 5:
                TreinoUI.Excluir()
            elif opcao == 6:
                TreinoUI.MaisRapido()
            elif opcao == 7:
                print("Saindo")
                break
            else:
                print("Opção inválida")

    @staticmethod
    def Menu():
        print("\n--- Menu - Treino ---")
        print("1. Inserir novo treino")
        print("2. Listar treinos")
        print("3. Listar treino pelo id")
        print("4. Atualizar dados do treino")
        print("5. Excluir treino")
        print("6. Encontrar o treino de maior velocidade")
        print("7. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def Inserir():
        try:
            id = int(input("ID: "))
            data_str = input("Data do treino (dd/mm/aaaa): ")
            data = datetime.strptime(data_str, "%d/%m/%Y")
            distancia = input("Distância percorrida: ")
            h,m,s = map(int, input("Tempo da corrida").split(""))
            tempo = timedelta(hours=h, minutes=m, seconds=s)
            treino = Treino(id, data, distancia, tempo)
            TreinoUI.treinos.append(treino)
            print("Treino inserido com sucesso")
        except Exception as e:
            print(f"Erro ao inserir treino: {e}")

    @staticmethod
    def Listar():
        if not TreinoUI.treinos:
            print("Nenhum treino cadastrado.")
        else:
            for treino in TreinoUI.treinos:
                print(treino.ToString())

    @staticmethod
    def Atualizar():
        try:
            id = int(input("Informe o ID do treino a atualizar: "))
            treino = next((t for t in TreinoUI.treinos if t.get_id() == id), None)
            if treino:
                data_str = input(f"Nova data da corrida ({treino.get_data().strftime('%d/%m/%Y')}): ")
                data = treino.get_data()
                distancia = float(input(f"Nova distãncia percorrida ({treino.get_distancia()}): ")) or treino.get_distancia()
                 = float(input(f"Nova distância percorrida ({treino.get_distancia()}): ")) or treino.get_distancia()
                if data_str:
                    data = datetime.strptime(data_str, "%d/%m/%Y")
                treino.set_data(data)
                treino.set_distancia(distancia)
                treino.set_tempo(tempo)
                print("Treino atualizado com sucesso")
            else:
                print("Treino não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar treino: {e}")

    @staticmethod
    def Excluir():
        try:
            id = int(input("Informe o ID do contato a excluir: "))
            contato = next((c for c in ContatoUI.contatos if c.get_id() == id), None)
            if contato:
                ContatoUI.contatos.remove(contato)
                print("Contato excluído com sucesso")
            else:
                print("Contato não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir contato: {e}")

    @staticmethod
    def Pesquisar():
        iniciais = input("Informe as iniciais do nome: ").lower()
        encontrados = [c for c in ContatoUI.contatos if c.get_nome().lower().startswith(iniciais)]
        if encontrados:
            for contato in encontrados:
                print(contato.ToString())
        else:
            print("Nenhum contato encontrado com essas iniciais.")

    @staticmethod
    def Aniversariantes():
        try:
            mes = int(input("Informe o mês (1-12): "))
            aniversariantes = [c for c in ContatoUI.contatos if c.get_nascimento().month == mes]
            if aniversariantes:
                print(f"Contatos que fazem aniversário em {mes}:")
                for contato in aniversariantes:
                    print(contato.ToString())
            else:
                print("Nenhum aniversariante neste mês.")
        except Exception as e:
            print(f"Erro ao buscar aniversariantes: {e}")

if __name__ == "__main__":
    ContatoUI.Main()