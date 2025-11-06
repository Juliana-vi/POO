from abc import ABC, abstractmethod
from models.cliente import Cliente
from models.profissional import Profissional
from models.horario import Horario, HorarioDAO
import json

class DAO(ABC):
  _objetos = []
  @classmethod
  def inserir(cls, obj):
    cls.abrir()
    id = 0
    for aux in cls._objetos:
      if aux.get_id() > id: id = aux.get_id()
    obj.set_id(id + 1)
    cls._objetos.append(obj)
    cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.__objetos()
    
    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.__objetos:
            if obj.get_id() == id:
                return obj
        return None
    
    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.__objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux != None:
            cls.__objetos.remove(aux)
            cls.salvar()
    
    @staticmethod
    def alterar_senha(id_cliente, senha_antiga, nova_senha):
        lista = Cliente.abrir()
        for c in lista:
            if c._Cliente__id == id_cliente and c._Cliente__senha == senha_antiga:
                c._Cliente__senha = nova_senha
                Cliente.salvar(lista)
                return True
        return False
    
    @staticmethod
    def alterar_senha(id_prof, senha_antiga, nova_senha):
        lista = Profissional.abrir()
        for p in lista:
            if p._Profissional__id == id_prof and p._Profissional__senha == senha_antiga:
                p._Profissional__senha = nova_senha
                Profissional.salvar(lista)
                return True
        return False
    
    @staticmethod
    def listar_agenda_cliente(id_cliente):
        lista = HorarioDAO.abrir()
        return [a for a in lista if a._AgendarServico__id_cliente == id_cliente]

    @staticmethod
    def listar_agenda_profissional(id_prof):
        lista = HorarioDAO.abrir()
        return [a for a in lista if a._AgendarServico__id_profissional == id_prof]

    @staticmethod
    def confirmar_servico(id_agendamento):
        lista = HorarioDAO.abrir()
        for a in lista:
            if a._AgendarServico__id == id_agendamento:
                a._AgendarServico__confirmado = True
                HorarioDAO.salvar(lista)
                return True
        return False

    @staticmethod
    def filtrar_por_data(lista, data):
        return [a for a in lista if a._AgendarServico__data == data]

    @staticmethod
    def ordenar_por_data(lista, reverso=False):
        from datetime import datetime
        return sorted(lista, key=lambda a: datetime.strptime(a._AgendarServico__data, "%Y-%m-%d"), reverse=reverso)


    @classmethod
    @abstractmethod
    def abrir(cls):
      pass

    @classmethod
    @abstractmethod
    def salvar(cls):
      pass
