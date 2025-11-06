import json
from pathlib import Path
from models.dao import DAO

class Servico:
    def __init__(self, servico_id, descricao, valor):
        self.__id = servico_id
        self.__descricao = descricao
        self.__valor = valor

    def get_id(self): return self.__id
    def get_descricao(self): return self.__descricao
    def get_valor(self): return self.__valor

    def set_id(self, id):
        self.__id = id
        
    def set_descricao(self, descricao):
        if not descricao.strip():
            raise ValueError("Descrição inválida.")
        self.__descricao = descricao

    def set_valor(self, valor):
        if valor < 0:
            raise ValueError("Valor inválido.")
        self.__valor = valor

    def to_json(self):
        return {"id": self.__id, "descricao": self.__descricao, "valor": self.__valor}

    @staticmethod
    def from_json(dic):
        return Servico(dic.get("id", 0), dic.get("descricao", ""), dic.get("valor", 0.0))

class ServicoDAO(DAO):
    arquivo = str(Path(__file__).parent.parent / "servicos.json")

    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open(cls.arquivo, mode="r", encoding="utf-8") as arq:
                lista = json.load(arq)
                for dic in lista:
                    cls._objetos.append(Servico.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls._objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open(cls.arquivo, mode="w", encoding="utf-8") as arq:
                json.dump([o.to_json() for o in cls._objetos], arq, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar serviços: {e}")
