import json
from models.dao import DAO
from pathlib import Path

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
    arquivo = str(Path(__file__).parent.parent / "clientes.json")

    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open(cls.arquivo, mode="r", encoding="utf-8") as arq:
                lista = json.load(arq)
                for dic in lista:
                    cls._objetos.append(Cliente.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls._objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open(cls.arquivo, mode="w", encoding="utf-8") as arq:
                json.dump([o.to_json() for o in cls._objetos], arq, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar clientes: {e}")

    # 🔹 Método específico: alterar senha
    @staticmethod
    def alterar_senha(id_cliente, senha_antiga, nova_senha):
        lista = ClienteDAO.listar()
        for c in lista:
            if c.get_id() == id_cliente and c.get_senha() == senha_antiga:
                c.set_senha(nova_senha)
                ClienteDAO.salvar()
                return True
        return False