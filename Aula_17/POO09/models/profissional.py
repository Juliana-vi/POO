import json

class Profissional:
    def __init__(self, prof_id, nome, especialidade, conselho, email, senha):
        self.__id = prof_id
        self.__nome = nome
        self.__especialidade = especialidade
        self.__conselho = conselho
        self.__email = email
        self.__senha = senha

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_conselho(self): return self.__conselho
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def set_nome(self, nome): self.__nome = nome
    def set_especialidade(self, especialidade): self.__especialidade = especialidade
    def set_conselho(self, conselho): self.__conselho = conselho
    def set_email(self, email): self.__email = email
    def set_senha(self, senha): self.__senha = senha

    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "especialidade": self.__especialidade,
            "conselho": self.__conselho,
            "email": self.__email,
            "senha": self.__senha
        }

    @staticmethod
    def from_json(dic):
        return Profissional(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )


class ProfissionalDAO:
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
            obj._Profissional__id = max_id + 1
        cls.__objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos.copy()

    @classmethod
    def listar_id(cls, prof_id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == prof_id:
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
            with open("profissionais.json", "r") as f:
                lista = json.load(f)
                for dic in lista:
                    cls.__objetos.append(Profissional.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("profissionais.json", "w") as f:
                json.dump([o.to_json() for o in cls.__objetos], f, indent=2)
        except Exception as e:
            print("Erro ao salvar profissionais:", e)

    @staticmethod
    def alterar_senha(id_prof, senha_antiga, nova_senha):
        lista = Profissional.abrir()
        for p in lista:
            if p._Profissional__id == id_prof and p._Profissional__senha == senha_antiga:
                p._Profissional__senha = nova_senha
                Profissional.salvar(lista)
                return True
        return False
