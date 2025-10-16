import json

class Cliente:
    def __init__(self, cliente_id, nome, email, fone, senha):
        self.__id = cliente_id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
        self.__senha = senha

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} – {self.__fone}"

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_fone(self): return self.__fone
    def get_senha(self): return self.__senha

    def set_id(self, cliente_id): self.__id = cliente_id
    def set_nome(self, nome): self.__nome = nome
    def set_email(self, email): self.__email = email
    def set_fone(self, fone): self.__fone = fone
    def set_senha(self, senha): self.__senha = senha

    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic):
        return Cliente(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("email", ""),
            dic.get("fone", ""),
            dic.get("senha", "")
        )


class ClienteDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        max_id = 0
        for aux in cls.__objetos:
            if aux.get_id() > max_id:
                max_id = aux.get_id()
        obj.set_id(max_id + 1)
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos.copy()

    @classmethod
    def listar_id(cls, cliente_id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == cliente_id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        existente = cls.listar_id(obj.get_id())
        if existente is not None:
            cls.__objetos.remove(existente)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        existente = cls.listar_id(obj.get_id())
        if existente is not None:
            cls.__objetos.remove(existente)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("clientes.json", "r") as f:
                lista = json.load(f)
                for dic in lista:
                    cls.__objetos.append(Cliente.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("clientes.json", "w") as f:
                json.dump([o.to_json() for o in cls.__objetos], f, indent=2)
        except Exception as e:
            print("Erro ao salvar clientes:", e)