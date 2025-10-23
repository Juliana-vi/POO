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

    @staticmethod
    def listar_por_profissional(id_prof):
        lista = Servico.abrir()
        return [s for s in lista if s._Servico__id_profissional == id_prof]

    @staticmethod
    def ordenar_por_nome(lista, reverso=False):
        return sorted(lista, key=lambda s: s._Servico__nome.lower(), reverse=reverso)

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

    @staticmethod
    def listar_agenda_cliente(id_cliente):
        lista = AgendarServico.abrir()
        return [a for a in lista if a._AgendarServico__id_cliente == id_cliente]

    @staticmethod
    def listar_agenda_profissional(id_prof):
        lista = AgendarServico.abrir()
        return [a for a in lista if a._AgendarServico__id_profissional == id_prof]

    @staticmethod
    def confirmar_servico(id_agendamento):
        lista = AgendarServico.abrir()
        for a in lista:
            if a._AgendarServico__id == id_agendamento:
                a._AgendarServico__confirmado = True
                AgendarServico.salvar(lista)
                return True
        return False

    @staticmethod
    def filtrar_por_data(lista, data):
        return [a for a in lista if a._AgendarServico__data == data]

    @staticmethod
    def ordenar_por_data(lista, reverso=False):
        from datetime import datetime
        return sorted(lista, key=lambda a: datetime.strptime(a._AgendarServico__data, "%Y-%m-%d"), reverse=reverso)
