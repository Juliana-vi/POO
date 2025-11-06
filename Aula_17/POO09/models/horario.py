from datetime import datetime
import json
from pathlib import Path
from models.dao import DAO

class Horario:
    def __init__(self, id, data):
        if isinstance(data, str):
            data = datetime.fromisoformat(data)
        if data.year < 2025:
            raise ValueError("Não é permitido cadastrar horários com data anterior a 2025.")
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0)

    def __str__(self):
        return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - {self.__confirmado}"

    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_confirmado(self): return self.__confirmado
    def get_id_cliente(self): return self.__id_cliente
    def get_id_servico(self): return self.__id_servico
    def get_id_profissional(self): return self.__id_profissional

    def set_id(self, id): self.__id = id
    def set_data(self, data): self.__data = data
    def set_confirmado(self, confirmado): self.__confirmado = confirmado
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.__id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional

    def to_json(self):
        return {
            "id": self.__id,
            "data": self.__data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.__confirmado,
            "id_cliente": self.__id_cliente,
            "id_servico": self.__id_servico,
            "id_profissional": self.__id_profissional
        }

    @staticmethod
    def from_json(dic):
        horario = Horario(dic["id"], datetime.strptime(dic["data"], "%d/%m/%Y %H:%M"))
        horario.set_confirmado(dic["confirmado"])
        horario.set_id_cliente(dic["id_cliente"])
        horario.set_id_servico(dic["id_servico"])
        horario.set_id_profissional(dic.get("id_profissional", 0))
        return horario

class HorarioDAO(DAO):
    arquivo = str(Path(__file__).parent.parent / "horarios.json")

    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open(cls.arquivo, mode="r", encoding="utf-8") as arq:
                lista = json.load(arq)
                for dic in lista:
                    cls._objetos.append(Horario.from_json(dic))
        except (FileNotFoundError, json.JSONDecodeError):
            cls._objetos = []

    @classmethod
    def salvar(cls):
        try:
            with open(cls.arquivo, mode="w", encoding="utf-8") as arq:
                json.dump([o.to_json() for o in cls._objetos], arq, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar horários: {e}")

    # 🔹 Métodos específicos (mantidos do sistema original)
    @classmethod
    def listar_agenda_cliente(cls, id_cliente):
        return [h for h in cls.listar() if h.get_id_cliente() == id_cliente]

    @classmethod
    def listar_agenda_profissional(cls, id_prof):
        return [h for h in cls.listar() if h.get_id_profissional() == id_prof]

    @classmethod
    def confirmar_servico(cls, id_agendamento):
        horario = cls.listar_id(id_agendamento)
        if horario:
            horario.set_confirmado(True)
            cls.salvar()
            return True
        return False

    @classmethod
    def filtrar_por_data(cls, lista, data_str):
        return [h for h in lista if h.get_data().strftime("%d/%m/%Y %H:%M") == data_str]

    @classmethod
    def ordenar_por_data(cls, lista, reverso=False):
        return sorted(lista, key=lambda h: h.get_data(), reverse=reverso)