import json

class Profissional:
    def __init__(self, id: int, nome: str, especialidade: str, conselho: str, email: str, senha: str):
        self.set_id(id)
        self.set_nome(nome)
        self.set_especialidade(especialidade)
        self.set_conselho(conselho)
        self.set_email(email)
        self.set_senha(senha)

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_conselho(self): return self.__conselho
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_especialidade(self, especialidade): self.__especialidade = especialidade
    def set_conselho(self, conselho): self.__conselho = conselho
    def set_email(self, email): self.__email = email
    def set_senha(self, senha): self.__senha = senha

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__especialidade} - {self.__conselho} - {self.__email}"

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
    __profissionais = []

    @classmethod
    def inserir(cls, profissional):
        cls.listar()
        id = 1
        if len(cls.__profissionais) > 0:
            id = cls.__profissionais[-1].get_id() + 1
        profissional.set_id(id)
        cls.__profissionais.append(profissional)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__profissionais

    @classmethod
    def atualizar(cls, profissional):
        cls.listar()
        for i, p in enumerate(cls.__profissionais):
            if p.get_id() == profissional.get_id():
                cls.__profissionais[i] = profissional
                break
        cls.salvar()

    @classmethod
    def excluir(cls, profissional):
        cls.listar()
        cls.__profissionais = [p for p in cls.__profissionais if p.get_id() != profissional.get_id()]
        cls.salvar()

    @classmethod
    def salvar(cls):
        with open("profissionais.json", "w") as f:
            json.dump([p.to_json() for p in cls.__profissionais], f)

    @classmethod
    def abrir(cls):
        try:
            with open("profissionais.json", "r") as f:
                cls.__profissionais = [Profissional.from_json(d) for d in json.load(f)]
        except Exception:
            cls.__profissionais = []
