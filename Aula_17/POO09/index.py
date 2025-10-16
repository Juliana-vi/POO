
from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.abrircontaUI import AbrirContaUI
from templates.loginUI import LoginUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.perfilprofissionalUI import PerfilProfissionalUI
from templates.agendarservicoUI import AgendarServicoUI
from views import View
import streamlit as st

class IndexUI:
  def menu_admin():
    op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Serviços", "Cadastro de Horários", "Cadastro de Profissionais"])
    if op == "Cadastro de Clientes":
      ManterClienteUI.main()
    if op == "Cadastro de Serviços":
      ManterServicoUI.main()
    if op == "Cadastro de Horários":
      ManterHorarioUI.main()
    if op == "Cadastro de Profissionais":
      ManterProfissionalUI.main()

  def menu_visitante():
    op = st.sidebar.selectbox("Menu", ["Entrar como Cliente", "Entrar como Profissional","Abrir Conta"])
    if op == "Entrar como Cliente": LoginUI.cliente()
    if op == "Entrar como Profissional": LoginUI.profissional()
    if op == "Abrir Conta": AbrirContaUI.main()

  def menu_cliente():
    op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço"])
    if op == "Meus Dados": PerfilClienteUI.main()
    if op == "Agendar Serviço": AgendarServicoUI.main()

  def menu_profissional():
        op = st.sidebar.selectbox("Menu", ["Meus Dados"])
        if op == "Meus Dados": PerfilProfissionalUI.main()

  def sair_do_sistema():
    if st.sidebar.button("Sair"):
      del st.session_state["usuario_id"]
      del st.session_state["usuario_nome"]
      st.rerun()

  def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state["usuario_nome"] == "admin"
            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"])
            if admin: IndexUI.menu_admin()
            else: 
                if st.session_state["usuario_tipo"] == "c": IndexUI.menu_cliente()
                elif st.session_state["usuario_tipo"] == "p": IndexUI.menu_profissional()
            IndexUI.sair_do_sistema()
  def main():
      View.cliente_criar_admin()
      IndexUI.sidebar()
  
IndexUI.main()