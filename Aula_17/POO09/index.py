import streamlit as st
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

class IndexUI:

    @staticmethod
    def menu_admin():
        st.sidebar.markdown("Menu do Administrador")

        op = st.sidebar.selectbox("Selecione uma opção:", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Cadastro de Profissionais"
        ])

        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        elif op == "Cadastro de Serviços":
            ManterServicoUI.main()
        elif op == "Cadastro de Horários":
            ManterHorarioUI.main()
        elif op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()

        st.sidebar.divider()
        if st.sidebar.button("Alterar Senha"):
            IndexUI.alterar_senha_admin()

    @staticmethod
    def alterar_senha_admin():
      st.subheader("Alterar Senha do Administrador")
      st.info("O e-mail do administrador não pode ser alterado.")

      id_admin = st.session_state["usuario_id"]

      nova = st.text_input("Digite a nova senha", type="password")

      if st.button("Salvar Nova Senha"):
         if View.alterar_senha(id_admin, nova, "a"):  
            st.success("Senha alterada com sucesso!")
         else:
            st.error("Erro ao alterar senha.")



    @staticmethod
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", [
            "Entrar como Cliente",
            "Entrar como Profissional",
            "Abrir Conta"
        ])

        if op == "Entrar como Cliente":
            LoginUI.cliente()
        elif op == "Entrar como Profissional":
            LoginUI.profissional()
        elif op == "Abrir Conta":
            AbrirContaUI.main()

    @staticmethod
    def menu_cliente():
        op = st.sidebar.selectbox("Menu do Cliente", [
            "Meus Dados",
            "Agendar Serviço"
        ])

        if op == "Meus Dados":
            PerfilClienteUI.main()
        elif op == "Agendar Serviço":
            AgendarServicoUI.main()

    @staticmethod
    def menu_profissional():
        op = st.sidebar.selectbox("Menu do Profissional", [
            "Meus Dados"
        ])

        if op == "Meus Dados":
            PerfilProfissionalUI.main()

    @staticmethod
    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            for chave in ["usuario_id", "usuario_nome", "usuario_tipo"]:
                if chave in st.session_state:
                    del st.session_state[chave]
            st.success("Você saiu do sistema.")
            st.rerun()

    @staticmethod
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            st.sidebar.markdown(f"Bem-vindo(a), **{st.session_state['usuario_nome']}**!")
            tipo = st.session_state.get("usuario_tipo")
            if st.session_state.get("usuario_nome") == "admin":
                IndexUI.menu_admin()
            elif tipo == "c":
                IndexUI.menu_cliente()
            elif tipo == "p":
                IndexUI.menu_profissional()
            else:
                st.error("Tipo de usuário inválido. Faça login novamente.")
                for chave in ["usuario_id", "usuario_nome", "usuario_tipo"]:
                    if chave in st.session_state:
                        del st.session_state[chave]
                st.rerun()
            IndexUI.sair_do_sistema()

    @staticmethod
    def main():
        st.title("Sistema de Agendamentos")
        IndexUI.sidebar()

if __name__ == "__main__":
    IndexUI.main()