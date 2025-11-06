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
        p = Path(cls.arquivo)
        if not p.exists():
            cls._objetos = []
            return cls._objetos
        try:
            with p.open("r", encoding="utf-8") as f:
                cls._objetos = json.load(f)
                return cls._objetos
        except Exception:
            cls._objetos = []
            return cls._objetos

    @classmethod
    def salvar(cls):
        p = Path(cls.arquivo)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump(cls._objetos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def listar_agenda_cliente(id_cliente):
        lista = HorarioDAO.abrir()
        def get_id_cliente(a):
            try:
                return a.get_id_cliente()
            except Exception:
                return a.get("id_cliente") if isinstance(a, dict) else getattr(a, "_AgendarServico__id_cliente", None)
        return [a for a in lista if get_id_cliente(a) == id_cliente]

    @staticmethod
    def listar_agenda_profissional(id_prof):
        lista = HorarioDAO.abrir()
        def get_id_prof(a):
            try:
                return a.get_id_profissional()
            except Exception:
                return a.get("id_profissional") if isinstance(a, dict) else getattr(a, "_AgendarServico__id_profissional", None)
        return [a for a in lista if get_id_prof(a) == id_prof]

    @staticmethod
    def confirmar_servico(id_agendamento):
        lista = HorarioDAO.abrir()
        changed = False
        for a in lista:
            aid = None
            try:
                aid = a.get_id()
            except Exception:
                aid = a.get("id") if isinstance(a, dict) else getattr(a, "_AgendarServico__id", None)
            if aid == id_agendamento:
                # marca confirmado
                if isinstance(a, dict):
                    a["confirmado"] = True
                else:
                    try:
                        a.set_confirmado(True)
                    except Exception:
                        setattr(a, "_AgendarServico__confirmado", True)
                changed = True
        if changed:
            HorarioDAO.salvar()
        return changed

    @staticmethod
    def filtrar_por_data(lista, data_str):
        return [a for a in lista if (a.get("data") if isinstance(a, dict) else getattr(a, "get_data", lambda: getattr(a, "_AgendarServico__data", None))()) == data_str]

    @staticmethod
    def ordenar_por_data(lista, reverso=False):
        def key(a):
            d = a.get("data") if isinstance(a, dict) else getattr(a, "get_data", lambda: getattr(a, "_AgendarServico__data", None))()
            return datetime.strptime(d, "%Y-%m-%d") if d else datetime.min
        return sorted(lista, key=key, reverse=reverso)