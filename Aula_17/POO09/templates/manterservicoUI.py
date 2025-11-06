import streamlit as st
from views import View
import time

class ManterServicoUI:
    @staticmethod
    def main():
        st.title("Cadastro de Serviços")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with tab1:
            ManterServicoUI.listar()
        with tab2:
            ManterServicoUI.inserir()
        with tab3:
            ManterServicoUI.atualizar()
        with tab4:
            ManterServicoUI.excluir()

    @staticmethod
    def listar():
        servicos = View.servico_listar()
        if not servicos:
            st.info("Nenhum serviço cadastrado ainda.")
            return

        dados = [{
            "ID": s.get_id(),
            "Descrição": s.get_descricao(),
            "Valor (R$)": f"{s.get_valor():.2f}"
        } for s in servicos]

        st.dataframe(dados, use_container_width=True)


    @staticmethod
    def inserir():
        descricao = st.text_input("Descrição do Serviço")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Inserir Serviço"):
            try:
                View.servico_inserir(descricao, float(valor))
                st.success("Serviço inserido com sucesso!")
            except ValueError as erro:
                st.error(erro)
            time.sleep(2)
            st.rerun()
            if descricao.strip():
                View.servico_inserir(descricao, valor)
                st.success("Serviço inserido com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha todos os campos.")

    @staticmethod
    def atualizar():
        servicos = View.servico_listar()
        if not servicos:
            st.warning("Nenhum serviço cadastrado.")
            return

        opcao = st.selectbox("Selecione o serviço:", [f"{s.get_id()} - {s.get_descricao()}" for s in servicos])
        id = int(opcao.split(" - ")[0])
        s = View.servico_listar_id(id)

        descricao = st.text_input("Nova descrição", value=s.get_descricao())
        valor = st.number_input("Novo valor", min_value=0.0, format="%.2f", value=s.get_valor())

        if st.button("Atualizar Serviço"):
            View.servico_atualizar(id, descricao, valor)
            st.success("Serviço atualizado com sucesso!")
            st.rerun()

    @staticmethod
    def excluir():
        servicos = View.servico_listar()
        if not servicos:
            st.warning("Nenhum serviço cadastrado.")
            return

        opcao = st.selectbox("Selecione o serviço para excluir:", [f"{s.get_id()} - {s.get_descricao()}" for s in servicos])
        id = int(opcao.split(" - ")[0])

        if st.button("Excluir Serviço"):
            try:
                id = op.get_id()
                View.servico_excluir(id)
                st.success("Serviço excluído com sucesso!")
            except ValueError as erro:
                st.error(erro)
            time.sleep(2)
            st.rerun()
