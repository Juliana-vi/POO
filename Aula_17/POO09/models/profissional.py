import json
import datetime
from pathlib import Path
from typing import List, Dict
from models.dao import DAO

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
        self.__avaliacoes: List[Dict] = []
        self.__media_avaliacoes = 0.0

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_especialidade(self): return self.__especialidade
    def get_conselho(self): return self.__conselho
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def set_id(self, i): self.__id = i
    def set_nome(self, nome): self.__nome = nome
    def set_especialidade(self, especialidade): self.__especialidade = especialidade
    def set_conselho(self, conselho): self.__conselho = conselho
    def set_email(self, email): self.__email = email
    def set_senha(self, senha): self.__senha = senha

    def add_avaliacao(self, id_cliente, nota, comentario):
        if not hasattr(self, "_avaliacoes") or self._avaliacoes is None:
            self._avaliacoes = []
        avaliacao = {
            "id_cliente": id_cliente,
            "cliente_id": id_cliente,
            "nota": float(nota),
            "comentario": comentario,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._avaliacoes.append(avaliacao)
        self._recalcular_media()

    def get_avaliacoes(self):
        return getattr(self, "_avaliacoes", []) or []

    def _recalcular_media(self):
        avals = self.get_avaliacoes()
        if not avals:
            self._media_avaliacoes = 0.0
            return
        total = sum(float(a.get("nota", 0)) for a in avals)
        self._media_avaliacoes = total / len(avals)

    def get_media_avaliacoes(self):
        return getattr(self, "_media_avaliacoes", 0.0)
# ...existing code...

    def to_json(self):
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
    def from_json(dic):
        p = Profissional(
            dic.get("id", 0),
            dic.get("nome", ""),
            dic.get("especialidade", ""),
            dic.get("conselho", ""),
            dic.get("email", ""),
            dic.get("senha", "")
        )
        p.__avaliacoes = dic.get("avaliacoes", [])
        p.__media_avaliacoes = dic.get("media_avaliacoes", 0.0)
        return p

class ProfissionalDAO(DAO):
    arquivo = str(Path(__file__).parent.parent / "profissionais.json")

    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open(cls.arquivo, mode="r", encoding="utf-8") as arq:
                lista = json.load(arq)
                for dic in lista:
                    cls._objetos.append(Profissional.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls._objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open(cls.arquivo, mode="w", encoding="utf-8") as arq:
                json.dump([o.to_json() for o in cls._objetos], arq, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar profissionais: {e}")

    # 🔹 Método específico: alterar senha
    @staticmethod
    def alterar_senha(id_prof, senha_antiga, nova_senha):
        lista = ProfissionalDAO.listar()
        for p in lista:
            if p.get_id() == id_prof and p.get_senha() == senha_antiga:
                p.set_senha(nova_senha)
                ProfissionalDAO.salvar()
                return True
        return False