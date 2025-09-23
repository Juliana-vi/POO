from models.servico import Servico, ServicoDAO

class View:
  def servico_listar():
    return ServicoDAO.listar()
  def servico_inserir(descricao, valor):
    servico = Servico(0, descricao, valor)
    ServicoDAO.inserir(servico)
  def servico_atualizar(id, descricao, valor):
    servico = Servico(id, descricao, valor)
    ServicoDAO.atualizar(servico)
  def servico_excluir(id):
    servico = Servico(id, "", "", "")
    ServicoDAO.excluir(servico)