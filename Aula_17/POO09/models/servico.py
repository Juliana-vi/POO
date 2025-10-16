import json

class Servico:
    def __init__(self, servico_id, descricao, valor):
        self.__id = servico_id
        self.__descricao = descricao
        self.__valor = valor

    def get_id(self): return self.__id
    def get_descricao(self): return self.__descricao
    def get_valor(self): return self.__valor

    def set_descricao(self, descricao): self.__descricao = descricao
    def set_valor(self, valor): self.__valor = valor

    def to_json(self):
        return {"id": self.__id, "descricao": self.__descricao, "valor": self.__valor}

    @staticmethod
    def from_json(dic):
        return Servico(dic.get("id", 0), dic.get("descricao", ""), dic.get("valor", 0))


class ServicoDAO:
    __objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        max_id = 0
        for aux in cls.__objetos:
            if aux.get_id() > max_id:
                max_id = aux.get_id()
        try:
            obj.set_id(max_id + 1)
        except AttributeError:
            obj._Servico__id = max_id + 1
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos.copy()

    @classmethod
    def listar_id(cls, servico_id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == servico_id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        existente = cls.listar_id(obj.get_id())
        if existente:
            cls.__objetos.remove(existente)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        existente = cls.listar_id(obj.get_id())
        if existente:
            cls.__objetos.remove(existente)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("servicos.json", "r") as f:
                lista = json.load(f)
                for dic in lista:
                    cls.__objetos.append(Servico.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("servicos.json", "w") as f:
                json.dump([o.to_json() for o in cls.__objetos], f, indent=2)
        except Exception as e:
            print("Erro ao salvar servicos:", e)