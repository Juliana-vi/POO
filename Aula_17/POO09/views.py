from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO

class View:
  def cliente_listar():
    return ClienteDAO.listar()
  
  def cliente_inserir(nome, email, fone):
    cliente = Cliente(0, nome, email, fone)
    ClienteDAO.inserir(cliente)

  def cliente_atualizar(id, nome, email, fone):
    cliente = Cliente(id, nome, email, fone)
    ClienteDAO.atualizar(cliente)

  def cliente_excluir(id):
    cliente = Cliente(id, "", "", "")
    ClienteDAO.excluir(cliente)

  @staticmethod
  def cliente_listar_id(id):
    clientes = View.cliente_listar()
    for cliente in clientes:
      if cliente.get_id() == id:
        return cliente
    return None

  def servico_listar():
    return ServicoDAO.listar()
  
  def servico_inserir(descricao, valor):
    servico = Servico(0, descricao, valor)
    ServicoDAO.inserir(servico)

  def servico_atualizar(id, descricao, valor):
    servico = Servico(id, descricao, valor)
    ServicoDAO.atualizar(servico)

  def servico_excluir(id):
    servico = Servico(id, "", 0.0)
    ServicoDAO.excluir(servico)

  @staticmethod
  def servico_listar_id(id):
    servicos = View.servico_listar()
    for servico in servicos:
      if servico.get_id() == id:
        return servico
    return None

  def horario_inserir(data, confirmado, id_cliente, id_servico):
    c = Horario(0, data)
    c.set_confirmado(confirmado)
    c.set_id_cliente(id_cliente)
    c.set_id_servico(id_servico)
    HorarioDAO.inserir(c)

  def horario_listar():
    return HorarioDAO.listar()
  
  def horario_atualizar(id, data, confirmado, id_cliente, id_servico):
    c= Horario(id, data)
    c.set_confirmado(confirmado)
    c.set_id_cliente(id_cliente)
    c.set_id_servico(id_servico)
    HorarioDAO.atualizar(c)

  def horario_excluir(id):
    c = Horario(id, None)
    HorarioDAO.excluir(c)
