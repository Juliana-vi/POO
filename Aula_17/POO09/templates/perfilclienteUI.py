import streamlit as st
from views import View

class PerfilClienteUI:
  def main():
    st.header("Meu Perfil")
    if "usuario_id" not in st.session_state:
      st.info("Faça login para acessar seu perfil.")
      return

    user_id = st.session_state["usuario_id"]
    user_tipo = st.session_state.get("usuario_tipo", "cliente")

    if user_tipo == "cliente":
      op = View.cliente_listar_id(user_id)
      if op is None:
        st.error("Cliente não encontrado.")
        return
      nome = st.text_input("Informe o novo nome", op.get_nome)
      email = st.text_input("Informe o novo e-mail", op.get_email())
      fone = st.text_input("Informe o novo fone", op.get_fone())
      senha = st.text_input("Informe a nova senha", op.get_senha(), type="password")
      if st.button("Atualizar"):
        View.cliente_atualizar(op.get_id(), nome, email, fone, senha)
        st.success("Cliente atualizado com sucesso")
    else:
      op = View.profissional_listar_id(user_id)
      if op is None:
        st.error("Profissional não encontrado.")
        return
      nome = st.text_input("Informe o novo nome", op.get_nome())
      especialidade = st.text_input("Informe a nova especialidade", op.get_especialidade())
      conselho = st.text_input("Informe o novo conselho", op.get_conselho())
      email = st.text_input("Informe o novo e-mail", op.get_email())
      senha = st.text_input("Informe a nova senha", op.get_senha(), type="password")
      if st.button("Atualizar Perfil"):
        View.profissional_atualizar(op.get_id(), nome, especialidade, conselho, email, senha)
        st.success("Profissional atualizado com sucesso")
