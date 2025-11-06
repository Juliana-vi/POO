from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any, List

class DAO(ABC):
  _objetos: List[Any] = []

  @classmethod
  def inserir(cls, obj):
    cls.abrir()
    max_id = 0
    for aux in cls._objetos:
      try:
        aid = aux.get_id()
      except Exception:
        aid  = getattr(aux, "_id", 0)
      if aid and aid > max_id: max_id = aid
    try:
      obj.set_id(max_id + 1)
    except Exception:
        setattr(obj, "_id", max_id + 1)
    cls._objetos.append(obj)
    cls.salvar()

    @classmethod
    def listar(cls) -> List[Any]:
        cls.abrir()
        return cls._objetos 
    
    @classmethod
    def listar_id(cls, id: int) -> Optional[Any]:
        cls.abrir()
        for obj in cls._objetos:
            try:
                if obj.get_id() == id:
                    return obj
            except Exception:
                if getattr(obj, "_id", None) == id:
                    return obj
        return None

    
    @classmethod
    def atualizar(cls, obj: Any):
        aux = cls.listar_id(getattr(obj, "get_id", lambda: getattr(obj, "_id", None))())
        if aux is not None:
            cls._objetos.remove(aux)
            cls._objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj: Any):
        aux = cls.listar_id(getattr(obj, "get_id", lambda: getattr(obj, "_id", None))())
        if aux is not None:
            cls._objetos.remove(aux)
            cls.salvar()

    @classmethod
    @abstractmethod
    def abrir(cls):
        pass

    @classmethod
    @abstractmethod
    def salvar(cls):
        pass