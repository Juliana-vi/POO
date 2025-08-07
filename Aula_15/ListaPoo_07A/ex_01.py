import json

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

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "email": self._email,
            "fone": self._fone
        }

    def ToString(self):
        return f"ID: {self._id} | Nome: {self._nome} | Email: {self._email} | Fone: {self._fone}"

class ClienteDAO:
    _objetos = []

    @classmethod
    def Inserir(cls, obj: Cliente):
        cls._Abrir()
        cls._objetos.append(obj)
        cls._Salvar()

    @classmethod
    def Listar(cls):
        cls._Abrir()
        return cls._objetos

    @classmethod
    def Listar_Id(cls, id: int):
        cls._Abrir()
        for c in cls._objetos:
            if c.get_id() == id:
                return c
        return None

    @classmethod
    def Atualizar(cls, obj: Cliente):
        cls._Abrir()
        for i, c in enumerate(cls._objetos):
            if c.get_id() == obj.get_id():
                cls._objetos[i] = obj
                cls._Salvar()
                return True
        return False

    @classmethod
    def Excluir(cls, obj: Cliente):
        cls._Abrir()
        cls._objetos = [c for c in cls._objetos if c.get_id() != obj.get_id()]
        cls._Salvar()

    @classmethod
    def _Abrir(cls):
        try:
            with open("clientes.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                cls._objetos = [Cliente(**d) for d in data]
        except FileNotFoundError:
            cls._objetos = []

    @classmethod
    def _Salvar(cls):
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in cls._objetos], f, ensure_ascii=False, indent=2)

class View:
    @staticmethod
    def Cliente_Listar():
        return ClienteDAO.Listar()

    @staticmethod
    def Cliente_Inserir(nome: str, email: str, fone: str):
        clientes = ClienteDAO.Listar()
        novo_id = max([c.get_id() for c in clientes], default=0) + 1
        cliente = Cliente(novo_id, nome, email, fone)
        ClienteDAO.Inserir(cliente)

    @staticmethod
    def Cliente_Atualizar(id: int, nome: str, email: str, fone: str):
        cliente = Cliente(id, nome, email, fone)
        return ClienteDAO.Atualizar(cliente)

    @staticmethod
    def Cliente_Excluir(id: int):
        cliente = ClienteDAO.Listar_Id(id)
        if cliente:
            ClienteDAO.Excluir(cliente)
            return True
        return False

class UI:
    @staticmethod
    def Main():
        while True:
            op = UI.Menu()
            if op == 1:
                UI.Cliente_Inserir()
            elif op == 2:
                UI.Cliente_Listar()
            elif op == 3:
                UI.Cliente_Atualizar()
            elif op == 4:
                UI.Cliente_Excluir()
            elif op == 5:
                print("Saindo")
                break
            else:
                print("Opção inválida")

    @staticmethod
    def Menu():
        print("\n--- Menu ---")
        print("1. Inserir novo cliente")
        print("2. Listar todos os clientes")
        print("3. Atualizar cliente")
        print("4. Excluir cliente")
        print("5. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def Cliente_Listar():
        clientes = View.Cliente_Listar()
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for c in clientes:
                print(c.ToString())

    @staticmethod
    def Cliente_Inserir():
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Fone: ")
        View.Cliente_Inserir(nome, email, fone)
        print("Cliente inserido com sucesso.")

    @staticmethod
    def Cliente_Atualizar():
        try:
            id = int(input("ID do cliente a atualizar: "))
        except ValueError:
            print("ID inválido.")
            return
        cliente = ClienteDAO.Listar_Id(id)
        if not cliente:
            print("Cliente não encontrado.")
            return
        nome = input(f"Nome [{cliente.get_nome()}]: ") or cliente.get_nome()
        email = input(f"Email [{cliente.get_email()}]: ") or cliente.get_email()
        fone = input(f"Fone [{cliente.get_fone()}]: ") or cliente.get_fone()
        if View.Cliente_Atualizar(id, nome, email, fone):
            print("Cliente atualizado com sucesso.")
        else:
            print("Erro ao atualizar cliente.")

    @staticmethod
    def Cliente_Excluir():
        try:
            id = int(input("ID do cliente a excluir: "))
        except ValueError:
            print("ID inválido.")
            return
        if View.Cliente_Excluir(id):
            print("Cliente excluído com sucesso.")
        else:
            print("Cliente não encontrado.")

if __name__ == "__main__":
    UI.Main()