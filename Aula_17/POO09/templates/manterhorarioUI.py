import streamlit as st
from views import View
from datetime import datetime

class ManterHorarioUI:
    @staticmethod
    def main():
        st.title("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with tab1:
            ManterHorarioUI.listar()
        with tab2:
            ManterHorarioUI.inserir()
        with tab3:
            ManterHorarioUI.atualizar()
        with tab4:
            ManterHorarioUI.excluir()

    @staticmethod
    def listar():
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
        else:
            for h in horarios:
                st.write(
                    f"**ID:** {h.get_id()} | **Data:** {h.get_data()}"
                    f"**Profissional:** {h.get_profissional().get_nome()} | **Cliente:** {h.get_cliente().get_nome() if h.get_cliente() else '—'}"
                )

    @staticmethod
    def inserir():
        profissionais = View.profissional_listar()
        clientes = View.cliente_listar()

        if not profissionais:
            st.warning("Nenhum profissional cadastrado. Cadastre um antes de inserir horários.")
            return

        data = st.date_input("Data do atendimento")
        hora = st.time_input("Hora do atendimento")
        profissional = st.selectbox("Profissional", [f"{p.get_id()} - {p.get_nome()}" for p in profissionais])

        id_prof = int(profissional.split(" - ")[0])
        id_cliente = None

        if clientes:
            cliente_opcional = st.selectbox("Cliente (opcional)", ["— Nenhum —"] + [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
            if cliente_opcional != "— Nenhum —":
                id_cliente = int(cliente_opcional.split(" - ")[0])

        if st.button("Inserir Horário"):
            View.horario_inserir(data.strftime("%Y-%m-%d"), hora.strftime("%H:%M"), id_prof, id_cliente)
            st.success("Horário inserido com sucesso!")
            st.rerun()

    @staticmethod
    def atualizar():
        horarios = View.horario_listar()
        if not horarios:
            st.warning("Nenhum horário cadastrado.")
            return

        opcao = st.selectbox("Selecione o horário:", [f"{h.get_id()} - {h.get_data()} {h.get_hora()}" for h in horarios])
        id = int(opcao.split(" - ")[0])
        h = View.horario_listar_id(id)

        data = st.date_input("Nova data", value=datetime.strptime(h.get_data(), "%Y-%m-%d"))
        hora = st.time_input("Nova hora", value=datetime.strptime(h.get_hora(), "%H:%M").time())

        profissionais = View.profissional_listar()
        clientes = View.cliente_listar()

        profissional = st.selectbox("Novo profissional", [f"{p.get_id()} - {p.get_nome()}" for p in profissionais], 
                                    index=[p.get_id() for p in profissionais].index(h.get_profissional().get_id()))

        cliente_opcional = st.selectbox("Novo cliente (opcional)", ["— Nenhum —"] + [f"{c.get_id()} - {c.get_nome()}" for c in clientes])
        id_prof = int(profissional.split(" - ")[0])
        id_cliente = None if cliente_opcional == "— Nenhum —" else int(cliente_opcional.split(" - ")[0])

        if st.button("Atualizar Horário"):
            View.horario_atualizar(id, data.strftime("%Y-%m-%d"), hora.strftime("%H:%M"), id_prof, id_cliente)
            st.success("Horário atualizado com sucesso!")
            st.rerun()

    @staticmethod
    def excluir():
        horarios = View.horario_listar()
        if not horarios:
            st.warning("Nenhum horário cadastrado.")
            return

        opcao = st.selectbox("Selecione o horário para excluir:", [f"{h.get_id()} - {h.get_data()} {h.get_hora()}" for h in horarios])
        id = int(opcao.split(" - ")[0])

        if st.button("Excluir Horário"):
            View.horario_excluir(id)
            st.success("Horário excluído com sucesso!")
            st.rerun()
