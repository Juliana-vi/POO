import json
from models.dao import DAO

class Cliente:
    def __init__(self, cliente_id, nome, email, fone, senha):
        if not nome or not email or not senha:
            raise ValueError("Cliente deve ter nome, email e senha válidos.")
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
    def set_nome(self, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = nome
    def set_email(self, email):
        if not email:
            raise ValueError("Email não pode ser vazio.")
        self.__email = email
    def set_fone(self, fone): self.__fone = fone
    def set_senha(self, senha):
        if not senha:
            raise ValueError("Senha não pode ser vazia.")
        self.__senha = senha


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

class ClienteDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("clientes.json", mode= "r") as arquivo:
                lista = json.load(arquivo)
                for dic in lista:
                    try:
                      cls.__objetos.append(Cliente.from_json(dic))
                    except ValueError:
                      print(f"[AVISO] Cliente inválido ignorado: {dic}")
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("clientes.json", mode= "w") as arquivo:
                json.dump([o.to_json() for o in cls.__objetos], arquivo, indent=2)
        except Exception as e:
            print("Erro ao salvar clientes:", e)
