import csv

class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str):
        self._id = id
        self._nome = nome
        self._email = email
        self._fone = fone

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def get_fone(self):
        return self._fone

    def set_nome(self, nome):
        self._nome = nome

    def set_email(self, email):
        self._email = email

    def set_fone(self, fone):
        self._fone = fone

    def ToString(self):
        return f"ID: {self._id}\nNome: {self._nome}\nE-mail: {self._email}\nFone: {self._fone}\n"

class ClienteUI:
    objetos = []

    @staticmethod
    def main():
        while True:
            opcao = ClienteUI.menu()
            if opcao == 1:
                ClienteUI.inserir()
            elif opcao == 2:
                ClienteUI.listar()
            elif opcao == 3:
                ClienteUI.listar_id()
            elif opcao == 4:
                ClienteUI.atualizar()
            elif opcao == 5:
                ClienteUI.excluir()
            elif opcao == 6:
                ClienteUI.abrir()
            elif opcao == 7:
                ClienteUI.salvar()
            elif opcao == 8:
                print("Saindo do sistema.")
                break
            else:
                print("Opção inválida")

    @staticmethod
    def menu():
        print("\n--- Cadastro de Clientes ---")
        print("1. Inserir novo cliente")
        print("2. Listar todos os clientes")
        print("3. Listar cliente por ID")
        print("4. Atualizar cliente")
        print("5. Excluir cliente")
        print("6. Abrir lista de clientes de um arquivo")
        print("7. Salvar lista de clientes em um arquivo")
        print("8. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def inserir():
        try:
            id = int(input("ID: "))
            nome = input("Nome: ")
            email = input("E-mail: ")
            fone = input("Fone: ")
            cliente = Cliente(id, nome, email, fone)
            ClienteUI.objetos.append(cliente)
            print("Cliente inserido com sucesso")
        except Exception as e:
            print(f"Erro ao inserir cliente: {e}")

    @staticmethod
    def listar():
        if not ClienteUI.objetos:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in ClienteUI.objetos:
                print(cliente.ToString())

    @staticmethod
    def listar_id():
        try:
            id = int(input("Informe o ID do cliente: "))
            cliente = next((c for c in ClienteUI.objetos if c.get_id() == id), None)
            if cliente:
                print(cliente.ToString())
            else:
                print("Cliente não encontrado.")
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")

    @staticmethod
    def atualizar():
        try:
            id = int(input("Informe o ID do cliente a atualizar: "))
            cliente = next((c for c in ClienteUI.objetos if c.get_id() == id), None)
            if cliente:
                nome = input(f"Novo nome ({cliente.get_nome()}): ") or cliente.get_nome()
                email = input(f"Novo e-mail ({cliente.get_email()}): ") or cliente.get_email()
                fone = input(f"Novo fone ({cliente.get_fone()}): ") or cliente.get_fone()
                cliente.set_nome(nome)
                cliente.set_email(email)
                cliente.set_fone(fone)
                print("Cliente atualizado com sucesso")
            else:
                print("Cliente não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")

    @staticmethod
    def excluir():
        try:
            id = int(input("Informe o ID do cliente a excluir: "))
            cliente = next((c for c in ClienteUI.objetos if c.get_id() == id), None)
            if cliente:
                ClienteUI.objetos.remove(cliente)
                print("Cliente excluído com sucesso")
            else:
                print("Cliente não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir cliente: {e}")

    @staticmethod
    def abrir():
        nome_arquivo = input("Nome do arquivo para abrir (ex: clientes.csv): ")
        try:
            with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                ClienteUI.objetos.clear()
                for row in reader:
                    if len(row) == 4:
                        id, nome, email, fone = row
                        ClienteUI.objetos.append(Cliente(int(id), nome, email, fone))
                print("Lista de clientes carregada com sucesso")
        except Exception as e:
            print(f"Erro ao abrir arquivo: {e}")

    @staticmethod
    def salvar():
        nome_arquivo = input("Nome do arquivo para salvar (ex: clientes.csv): ")
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for cliente in ClienteUI.objetos:
                    writer.writerow([cliente.get_id(), cliente.get_nome(), cliente.get_email(), cliente.get_fone()])
                print("Lista de clientes salva com sucesso")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

if __name__ == "__main__":
    ClienteUI.main()