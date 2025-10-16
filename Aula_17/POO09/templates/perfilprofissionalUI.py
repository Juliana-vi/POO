import streamlit as st
from views import View

class PerfilProfissionalUI:
    @staticmethod
    def main():
        id_profissional = st.session_state["usuario_id"]
        nome = st.session_state["usuario_nome"]

        st.title(f"Perfil do Profissional - {nome}")

        menu = st.selectbox("Selecione uma opção:", [
            "Abrir Agenda",
            "Visualizar Agenda",
            "Confirmar Serviços",
            "Alterar Senha"
        ])

        if menu == "Abrir Agenda":
            dias = st.number_input("Quantos dias de agenda deseja abrir?", 1, 30, 7)
            if st.button("Abrir Agenda"):
                View.profissional_abrir_agenda(id_profissional, dias)
                st.success("Agenda aberta com sucesso!")

        elif menu == "Visualizar Agenda":
            agenda = View.profissional_visualizar_agenda(id_profissional)
            if agenda:
                for h in agenda:
                    status = "Confirmado" if h.get_confirmado() else "Pendente"
                    cliente = (
                        View.cliente_listar_id(h.get_id_cliente()).get_nome()
                        if h.get_id_cliente()
                        else "(vago)"
                    )
                    st.write(f"- {h.get_data()} — {status} — Cliente: {cliente}")
            else:
                st.info("Nenhum horário criado ainda.")

        elif menu == "Confirmar Serviços":
            pendentes = [
                h for h in View.profissional_visualizar_agenda(id_profissional)
                if h.get_confirmado() == False and h.get_id_cliente() is not None
            ]
            if not pendentes:
                st.info("Nenhum serviço pendente para confirmar.")
            else:
                op = st.selectbox(
                    "Selecione um horário para confirmar:",
                    [f"{h.get_id()} - {h.get_data()}" for h in pendentes]
                )
                if st.button("Confirmar"):
                    id_horario = int(op.split(" - ")[0])
                    View.profissional_confirmar_servico(id_horario)
                    st.success("Serviço confirmado com sucesso!")

        elif menu == "Alterar Senha":
            nova = st.text_input("Digite a nova senha", type="password")
            if st.button("Salvar nova senha"):
                View.alterar_senha(id_profissional, nova, "p")
                st.success("Senha alterada com sucesso!")
