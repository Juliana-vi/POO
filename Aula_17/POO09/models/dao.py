from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any, List, Optional

class DAO(ABC):
    _objetos: List[Any] = []

    @classmethod
    def listar(cls) -> List[Any]:
        cls.abrir()
        return cls._objetos

    @classmethod
    def listar_id(cls, id: int) -> Optional[Any]:
        cls.abrir()
        for obj in cls._objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def inserir(cls, obj: Any):
        cls.abrir()
        max_id = 0
        for aux in cls._objetos:
            if aux.get_id() > max_id:
                max_id = aux.get_id()
        # garante que o objeto tenha set_id
        if hasattr(obj, "set_id"):
            obj.set_id(max_id + 1)
        cls._objetos.append(obj)
        cls.salvar()

    @classmethod
    def atualizar(cls, obj: Any):
        cls.abrir()
        antigo = cls.listar_id(obj.get_id())
        if antigo is not None:
            cls._objetos.remove(antigo)
            cls._objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj: Any):
        cls.abrir()
        antigo = cls.listar_id(obj.get_id())
        if antigo is not None:
            cls._objetos.remove(antigo)
            cls.salvar()

    @classmethod
    @abstractmethod
    def abrir(cls):
        pass

    @classmethod
    @abstractmethod
    def salvar(cls):
        pass
