import json
from models.horario import Horario 
from models.horario import HorarioDAO

class Servico:
    def __init__(self, servico_id, descricao, valor):
        self.__id = servico_id
        self.__descricao = descricao
        self.__valor = valor

    def get_id(self): return self.__id
    def get_descricao(self): return self.__descricao
    def get_valor(self): return self.__valor

    def set_descricao(self, descricao): 
        if descricao == "": raise ValueError("Descrição inválida") 
        self.__descricao = descricao
    def set_valor(self, valor): 
        if valor < 0: raise ValueError("Valor inválido")
        self.__valor = valor

    def to_json(self):
        return {"id": self.__id, "descricao": self.__descricao, "valor": self.__valor}

    @staticmethod
    def from_json(dic):
        return Servico(dic.get("id", 0), dic.get("descricao", ""), dic.get("valor", 0))


class ServicoDAO:
    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("servicos.json", mode="r") as arquivo:
                lista = json.load(arquivo)
                for dic in lista:
                    cls.__objetos.append(Servico.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("servicos.json",mode= "w") as arquivo:
                json.dump([o.to_json() for o in cls.__objetos], arquivo, indent=2)
        except Exception as e:
            print("Erro ao salvar servicos:", e)
