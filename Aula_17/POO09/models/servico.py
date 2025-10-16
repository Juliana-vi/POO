import json

class Servico:
    def __init__(self, id, descricao, valor):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_valor(valor)

    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao
    
    def get_valor(self):
        return self.__valor

    def set_id(self, id):
        self.__id = id

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_valor(self, valor):
        self.__valor = valor

    def __str__(self):
        return f"{self.__id} - {self.__descricao} - {self.__valor:.2f}"

    def to_json(self):
        return {"id": self.__id, "descricao": self.__descricao, "valor": self.__valor}

    @staticmethod
    def from_json(dic):
        return Servico(dic.get("id", 0), dic.get("descricao", ""), dic.get("valor", 0.0))


class ServicoDAO:
    __servicos = []

    @classmethod
    def inserir(cls, servico):
        cls.abrir()
        id = 1
        if len(cls.__servicos) > 0:
            id = cls.__servicos[-1].get_id() + 1
        servico.set_id(id)
        cls.__servicos.append(servico)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__servicos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for s in cls.__servicos:
            if s.get_id() == id:
                return s
        return None

    @classmethod
    def atualizar(cls, servico):
        cls.abrir()
        for i, s in enumerate(cls.__servicos):
            if s.get_id() == servico.get_id():
                cls.__servicos[i] = servico
                break
        cls.salvar()

    @classmethod
    def excluir(cls, servico):
        cls.abrir()
        cls.__servicos = [s for s in cls.__servicos if s.get_id() != servico.get_id()]
        cls.salvar()

    @classmethod
    def salvar(cls):
        with open("servicos.json", "w") as f:
            json.dump([s.to_json() for s in cls.__servicos], f, ensure_ascii=False, indent=2)

    @classmethod
    def abrir(cls):
        try:
            with open("servicos.json", "r") as f:
                cls.__servicos = [Servico.from_json(d) for d in json.load(f)]
        except Exception:
            cls.__servicos = []
