import streamlit as st
from views import View

class ManterClienteUI:
    @staticmethod
    def main():
        st.title("Cadastro de Clientes")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1:
            ManterClienteUI.listar()
        with tab2:
            ManterClienteUI.inserir()
        with tab3:
            ManterClienteUI.atualizar()
        with tab4:
            ManterClienteUI.excluir()

    @staticmethod
    def listar():
        clientes = View.cliente_listar()
        if not clientes:
            st.info("Nenhum cliente cadastrado.")
            return

        dados = [{
            "ID": c.get_id(),
            "Nome": c.get_nome(),
            "Email": c.get_email(),
            "Telefone": c.get_fone()
        } for c in clientes]

        st.dataframe(dados, use_container_width=True)

    @staticmethod
    def inserir():
        nome = st.text_input("Nome", key="cli_nome")
        email = st.text_input("Email", key="cli_email")
        fone = st.text_input("Fone", key="cli_fone")
        senha = st.text_input("Senha", type="password", key="cli_senha")
        if st.button("Inserir Cliente"):
            try:
              if not nome or not email:
                st.error("Nome e email obrigatórios.")
              else:
                View.cliente_inserir(nome, email, fone, senha)
                st.success("Cliente inserido.")
                st.rerun()
            except ValueError as e:
                st.error(f"Erro: {e}")

    @staticmethod
    def atualizar():
        clientes = View.cliente_listar()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
            return
        opcao = st.selectbox("Selecione cliente", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
        id_sel = int(opcao.split(" - ")[0])
        c = View.cliente_listar_id(id_sel)
        nome = st.text_input("Nome", value=c.get_nome())
        email = st.text_input("Email", value=c.get_email())
        fone = st.text_input("Fone", value=c.get_fone())
        senha = st.text_input("Senha (deixe em branco para manter)", type="password")
        if st.button("Atualizar Cliente"):
            try:
              View.cliente_atualizar(id_sel, nome, email, fone, senha if senha else c.get_senha())
              st.success("Cliente atualizado.")
              st.rerun()
            except ValueError as e:
                st.error(f"Erro: {e}")

    @staticmethod
    def excluir():
        clientes = View.cliente_listar()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
            return
        opcao = st.selectbox("Selecione cliente para excluir", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
        id_sel = int(opcao.split(" - ")[0])
        if st.button("Excluir Cliente"):
            try:
              View.cliente_excluir(id_sel)
              st.success("Cliente excluído.")
              st.rerun()
            except ValueError as e:
                st.error(f"Erro: {e}")
