from datetime import datetime

class Horario:
def __init__(self, id, data):

self.set_id(id)
self.set_data(data)
self.set_confirmado(False)

self.set_id_cliente(0)
self.set_id_servico(0)

def __str__(self):
return f"{self.__id}- self.__data.strftime('%d/%m/%Y %H:%M')}-{self.__confirmado}

def get_id(self): return self.__id
def get_data(self): return self.__data
def get_confirmado(self): return self.__confirmado
def get_id_cliente(self): return self.__id_cliente
def get_id_servico(self): return self.__id_servico

def set_id(self, id): self.__id = id
def set_data(self, data): self.__data = data
def set_confirmado(self, confirmado): self.__confirmado = confirmado
def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
def set_id_servico(self, id_servico): self.__id_servico = id_servico