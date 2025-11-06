import json
from typing import List, Dict

class Profissional:
    def __init__(self, prof_id, nome, especialidade, conselho, email, senha):
        if not nome or not email or not senha:
            raise ValueError("Profissional deve ter nome, email e senha válidos.")
        self.__id = prof_id
        self.__nome = nome
        self.__especialidade = especialidade
        self.__conselho = conselho
        self.__email = email
        self.__senha = senha
        self.__avaliacoes: List[Dict] = []  # Lista de avaliações {cliente_id, nota, comentario}
        self.__media_avaliacoes = 0.0

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

    def adicionar_avaliacao(self, cliente_id: int, nota: float, comentario: str) -> None:
        self.__avaliacoes.append({
            "cliente_id": cliente_id,
            "nota": nota,
            "comentario": comentario
        })
        self.__calcular_media()

    def __calcular_media(self) -> None:
        if not self.__avaliacoes:
            self.__media_avaliacoes = 0.0
            return
        total = sum(av["nota"] for av in self.__avaliacoes)
        self.__media_avaliacoes = total / len(self.__avaliacoes)

    def get_avaliacoes(self) -> List[Dict]:
        return self.__avaliacoes

    def get_media_avaliacoes(self) -> float:
        return self.__media_avaliacoes

    def to_json(self) -> Dict:
        return {
            "id": self.__id,
            "nome": self.__nome,
            "especialidade": self.__especialidade,
            "conselho": self.__conselho,
            "email": self.__email,
            "senha": self.__senha,
            "avaliacoes": self.__avaliacoes,
            "media_avaliacoes": self.__media_avaliacoes
        }

    @staticmethod
    def from_json(dic: dict) -> 'Profissional':
        prof = Profissional(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )
        prof.__avaliacoes = dic.get("avaliacoes", [])
        prof.__media_avaliacoes = dic.get("media_avaliacoes", 0.0)
        return prof


class ProfissionalDAO:
    @staticmethod
    def alterar_senha(id_prof, senha_antiga, nova_senha):
        lista = Profissional.abrir()
        for p in lista:
            if p._Profissional__id == id_prof and p._Profissional__senha == senha_antiga:
                p._Profissional__senha = nova_senha
                Profissional.salvar(lista)
                return True
        return False
    
    @classmethod
    def abrir(cls):
        cls.__objetos = []
        try:
            with open("profissionais.json", mode="r") as arquivo:
                lista = json.load(arquivo)
                for dic in lista:
                    try:
                       cls.__objetos.append(Profissional.from_json(dic))
                    except ValueError:
                      print(f"[AVISO] Profissional inválido ignorado: {dic}")
        except (FileNotFoundError, json.JSONDecodeError):
            cls.__objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open("profissionais.json", mode="w") as arquivo:
                json.dump([o.to_json() for o in cls.__objetos], arquivo, indent=2)
        except Exception as e:
            print("Erro ao salvar profissionais:", e)
