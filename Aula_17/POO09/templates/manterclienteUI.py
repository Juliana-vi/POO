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
            st.info("Nenhum cliente cadastrado ainda.")
        else:
            for c in clientes:
                st.write(
                    f"**ID:** {c.get_id()} | **Nome:** {c.get_nome()} | **E-mail:** {c.get_email()} | **Telefone:** {c.get_fone()}"
                )

    @staticmethod
    def inserir():
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        fone = st.text_input("Telefone")
        senha = st.text_input("Senha", type="password")

        if st.button("Inserir Cliente"):
            if nome and email and fone and senha:
                View.cliente_inserir(nome, email, fone, senha)
                st.success("Cliente inserido com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha todos os campos antes de inserir.")

    @staticmethod
    def atualizar():
        clientes = View.cliente_listar()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
            return

        opcao = st.selectbox("Selecione o cliente:", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
        id = int(opcao.split(" - ")[0])
        c = View.cliente_listar_id(id)

        nome = st.text_input("Novo nome", value=c.get_nome())
        email = st.text_input("Novo e-mail", value=c.get_email())
        fone = st.text_input("Novo telefone", value=c.get_fone())
        senha = st.text_input("Nova senha", value=c.get_senha(), type="password")

        if st.button("Atualizar Cliente"):
            View.cliente_atualizar(id, nome, email, fone, senha)
            st.success("Cliente atualizado com sucesso!")
            st.rerun()

    @staticmethod
    def excluir():
        clientes = View.cliente_listar()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
            return

        opcao = st.selectbox("Selecione o cliente para excluir:", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
        id = int(opcao.split(" - ")[0])

        if st.button("Excluir Cliente"):
            View.cliente_excluir(id)
            st.success("Cliente excluído com sucesso!")
            st.rerun()
