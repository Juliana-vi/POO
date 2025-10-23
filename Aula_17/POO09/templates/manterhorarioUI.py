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

    # ---------------- LISTAR ----------------
    @staticmethod
    def listar():
        horarios = View.horario_listar()
        if not horarios:
            st.info("Nenhum horário cadastrado ainda.")
            return

        dados = []
        for h in horarios:
            profissional = View.profissional_listar_id(h.get_id_profissional())
            cliente = View.cliente_listar_id(h.get_id_cliente())

            dados.append({
                "ID": h.get_id(),
                "Data": h.get_data(),
                "Confirmado": "Sim" if h.get_confirmado() else "Não",
                "Profissional": profissional.get_nome() if profissional else "—",
                "Cliente": cliente.get_nome() if cliente else "—"
            })

        st.dataframe(dados, use_container_width=True)

    # ---------------- INSERIR ----------------
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
            data_hora = datetime.combine(data, hora)
            View.horario_inserir(data_hora, False, id_cliente, None, id_prof)
            st.success("Horário inserido com sucesso!")
            st.rerun()

    # ---------------- ATUALIZAR ----------------
    @staticmethod
    def atualizar():
        horarios = View.horario_listar()
        if not horarios:
            st.warning("Nenhum horário cadastrado.")
            return

        opcao = st.selectbox("Selecione o horário:", [f"{h.get_id()} - {h.get_data()}" for h in horarios])
        id = int(opcao.split(" - ")[0])
        h = View.horario_listar_id(id)

        data = st.date_input("Nova data", value=h.get_data().date())
        hora = st.time_input("Nova hora", value=h.get_data().time())

        profissionais = View.profissional_listar()
        clientes = View.cliente_listar()

        # ⚙️ Correção robusta — evita erro se id_profissional for 0 ou inexistente
        prof_id_atual = h.get_id_profissional()
        ids_profissionais = [p.get_id() for p in profissionais]
        if prof_id_atual in ids_profissionais:
            idx_prof = ids_profissionais.index(prof_id_atual)
        else:
            idx_prof = 0

        profissional = st.selectbox(
            "Novo profissional",
            [f"{p.get_id()} - {p.get_nome()}" for p in profissionais],
            index=idx_prof
        )

        cliente_opcional = st.selectbox(
            "Novo cliente (opcional)",
            ["— Nenhum —"] + [f"{c.get_id()} - {c.get_nome()}" for c in clientes]
        )

        id_prof = int(profissional.split(" - ")[0])
        id_cliente = None if cliente_opcional == "— Nenhum —" else int(cliente_opcional.split(" - ")[0])

        if st.button("Atualizar Horário"):
            nova_data = datetime.combine(data, hora)
            View.horario_atualizar(
                id, 
                nova_data, 
                h.get_confirmado(), 
                id_cliente, 
                h.get_id_servico(), 
                id_prof
            )
            st.success("Horário atualizado com sucesso!")
            st.rerun()

    # ---------------- EXCLUIR ----------------
    @staticmethod
    def excluir():
        horarios = View.horario_listar()
        if not horarios:
            st.warning("Nenhum horário cadastrado.")
            return

        opcao = st.selectbox("Selecione o horário para excluir:", [f"{h.get_id()} - {h.get_data()}" for h in horarios])
        id = int(opcao.split(" - ")[0])

        if st.button("Excluir Horário"):
            View.horario_excluir(id)
            st.success("Horário excluído com sucesso!")
            st.rerun()
