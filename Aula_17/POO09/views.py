from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime, timedelta
from typing import List

class View:

    def cliente_criar_admin():
      clientes = ClienteDAO.listar()
      for c in clientes:
        if hasattr(c, "get_email") and c.get_email() == "admin":
            return
        elif isinstance(c, dict) and (c.get("email") == "admin" or c.get("_Cliente__email") == "admin"):
            return
    # se não existir, cria
    admin = Cliente(0, "admin", "admin", "fone", "1234")
    ClienteDAO.inserir(admin)


    @staticmethod
    def cliente_autenticar(email, senha):

      clientes = View.cliente_listar()

      def extrair(c):
        if hasattr(c, "get_email"):
            return c.get_email(), c.get_senha()
        elif isinstance(c, dict):
            return c.get("email") or c.get("_Cliente__email"), c.get("senha") or c.get("_Cliente__senha")
        return None, None

      if email == "admin":
        for c in clientes:
            em, pw = extrair(c)
            if em == "admin" and pw == senha:
                id_val = c.get_id() if hasattr(c, "get_id") else 0
                return {"id": id_val, "nome": "admin", "tipo": "a"}
        return None

      for c in clientes:
        em, pw = extrair(c)
        if em == email and pw == senha:
            id_val = c.get_id() if hasattr(c, "get_id") else None
            nome = c.get_nome() if hasattr(c, "get_nome") else em
            return {"id": id_val, "nome": nome, "tipo": "c"}

      return None

    def cliente_listar():
        r = ClienteDAO.listar()
        r.sort(key=lambda obj: obj.get_nome())
        return r

    def cliente_inserir(nome, email, fone, senha):
      if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios.")
      if email.lower() == "admin":
        raise ValueError("O e-mail 'admin' é reservado ao administrador.")
      for c in View.cliente_listar():
        if c.get_email().lower() == email.lower():
            raise ValueError("Já existe um cliente cadastrado com este e-mail.")
      cliente = Cliente(0, nome, email, fone, senha)
      ClienteDAO.inserir(cliente)


    def cliente_atualizar(id, nome, email, fone, senha):
      if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios.")
      if email.lower() == "admin":
        raise ValueError("O e-mail 'admin' é reservado ao administrador.")

      for c in View.cliente_listar():
        if c.get_email().lower() == email.lower() and c.get_id() != id:
            raise ValueError("Já existe um cliente cadastrado com este e-mail.")
      cliente = Cliente(id, nome, email, fone, senha)
      ClienteDAO.atualizar(cliente)


    def cliente_excluir(id):
      cliente = View.cliente_listar_id(id)
      if not cliente:
        raise ValueError("Cliente não encontrado.")
      for h in View.horario_listar():
        if h.get_id_cliente() == id:
            raise ValueError("Não é possível excluir cliente com horário agendado.")
      ClienteDAO.excluir(cliente)


    @staticmethod
    def cliente_listar_id(id):
        clientes = View.cliente_listar()
        for cliente in clientes:
            if cliente.get_id() == id:
                return cliente
        return None

    def servico_listar():
        r = ServicoDAO.listar()
        r.sort(key=lambda obj: obj.get_descricao())
        return r

    def servico_inserir(descricao, valor):
        for obj in View.servico_listar():
            if obj.get_descricao() == descricao:
                raise ValueError("Serviço já cadastrado.")
        c = Servico(0, descricao, valor)
        ServicoDAO.inserir(c)

    def servico_atualizar(id, descricao, valor):
        for obj in View.servico_listar():
            if obj.get_id() != id and obj.get_descricao() == descricao:
                raise ValueError("Descricão já cadastrada em outro servico.")
        c = Servico(id, descricao, valor)
        ServicoDAO.atualizar(c)

    def servico_excluir(id):
        for obj in View.horario_listar():
            if obj.get_id_servico() == id:
                raise ValueError("Servico já agendado: não é possível excluir.")
        c = Servico(id, "sem descrição", 0)
        ServicoDAO.excluir(c)

    @staticmethod
    def servico_listar_id(id):
        servicos = View.servico_listar()
        for servico in servicos:
            if servico.get_id() == id:
                return servico
        return None

    def horario_listar():
        r = HorarioDAO.listar()
        r.sort(key=lambda obj: obj.get_data())
        return r

    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
      if isinstance(data, str):
        try:
            data = datetime.strptime(data, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                data = datetime.strptime(data, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de data inválido. Use 'YYYY-MM-DD HH:MM' ou 'YYYY-MM-DD'.")

      if data.year < 2025:
        raise ValueError("Não é permitido cadastrar horários com data anterior a 2025.")

      for h in View.horario_listar():
        if h.get_id_profissional() == id_profissional and h.get_data() == data:
            raise ValueError("Já existe um horário para este profissional nesta data e hora.")

      c = Horario(0, data)
      c.set_confirmado(confirmado)
      c.set_id_cliente(id_cliente)
      c.set_id_servico(id_servico)
      c.set_id_profissional(id_profissional)
      HorarioDAO.inserir(c)


    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    data = datetime.strptime(data, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Formato de data inválido. Use 'YYYY-MM-DD HH:MM' ou 'YYYY-MM-DD'.")

        if data.year < 2025:
            raise ValueError("Não é permitido atualizar horários para datas anteriores a 2025.")

        for h in View.horario_listar():
            if h.get_id_profissional() == id_profissional and h.get_data() == data and h.get_id() != id:
                raise ValueError("Outro horário já existe para este profissional nesta data e hora.")

        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(c)

    def horario_excluir(id):
        h = View.horario_listar_id(id)
        if h.get_id_cliente() not in (None, 0):
            raise ValueError("Não é possível excluir um horário já agendado por um cliente.")
        HorarioDAO.excluir(h)
        
    def horario_listar_id(id):
        horario = HorarioDAO.listar_id(id)
        return horario

    def horario_agendar_horario(id_profissional):
        r = []
        agora = datetime.now()
        for h in View.horario_listar():
            if (
                h.get_data() >= agora and
                h.get_confirmado() == False and
                h.get_id_cliente() == None and
                h.get_id_profissional() == id_profissional
            ):
                r.append(h)
        r.sort(key=lambda h: h.get_data())
        return r

    def horario_filtrar_profissional(id_profissional):
        r = []
        for h in View.horario_listar():
            if h.get_id_profissional() == id_profissional:
                r.append(h)
        return r
    
    def filtrar_horarios_cliente(id_cliente, confirmado=None, data=None):
        horarios = [h for h in View.horario_listar() if h.get_id_cliente() == id_cliente]
        if confirmado is not None:
            horarios = [h for h in horarios if h.get_confirmado() == confirmado]
        if data:
            horarios = [h for h in horarios if h.get_data().date() == data]
        return sorted(horarios, key=lambda h: h.get_data())
    
    def filtrar_horarios_profissional(id_prof, confirmado=None, data=None):
        horarios = [h for h in View.horario_listar() if h.get_id_profissional() == id_prof]
        if confirmado is not None:
            horarios = [h for h in horarios if h.get_confirmado() == confirmado]
        if data:
            horarios = [h for h in horarios if h.get_data().date() == data]
        return sorted(horarios, key=lambda h: h.get_data())
    
    def confirmar_servico_profissional(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)
            return True
        return False


    def profissional_listar():
        r = ProfissionalDAO.listar()
        r.sort(key=lambda obj: obj.get_nome())
        return r

    def profissional_autenticar(email, senha):
        for p in View.profissional_listar():
            if p.get_email() == email and p.get_senha() == senha:
                return {"id": p.get_id(), "nome": p.get_nome()}
        return None

    def profissional_inserir(nome, especialidade, conselho, email, senha):
      if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios.")
      if email.lower() == "admin":
        raise ValueError("O e-mail 'admin' é reservado ao administrador.")
      for p in View.profissional_listar():
        if p.get_email().lower() == email.lower():
            raise ValueError("Já existe um profissional com este e-mail.")
      profissional = Profissional(0, nome, especialidade, conselho, email, senha)
      ProfissionalDAO.inserir(profissional)


    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
      if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios.")
      if email.lower() == "admin":
        raise ValueError("O e-mail 'admin' é reservado ao administrador.")

      for p in View.profissional_listar():
        if p.get_email().lower() == email.lower() and p.get_id() != id:
            raise ValueError("Já existe um profissional cadastrado com este e-mail.")
      profissional = Profissional(id, nome, especialidade, conselho, email, senha)
      ProfissionalDAO.atualizar(profissional)


    def profissional_excluir(id):
      for h in View.horario_listar():
        if h.get_id_profissional() == id:
            raise ValueError("Não é possível excluir profissional com horários agendados.")
      profissional = Profissional(id, '', '', '', '', '')
      ProfissionalDAO.excluir(profissional)

    @staticmethod
    def profissional_listar_id(id):
        profissionais = View.profissional_listar()
        for profissional in profissionais:
            if profissional.get_id() == id:
                return profissional
        return None

    @staticmethod
    def abrir_agenda(id_profissional, data_inicio, data_fim, hora_inicio, hora_fim, intervalo):
        data_atual = datetime.strptime(data_inicio, "%d/%m/%Y")
        data_limite = datetime.strptime(data_fim, "%d/%m/%Y")

        while data_atual <= data_limite:
            hora = datetime.strptime(hora_inicio, "%H:%M")
            fim = datetime.strptime(hora_fim, "%H:%M")

            while hora <= fim:
                data_completa = datetime.combine(data_atual.date(), hora.time())
                h = Horario(0, data_completa)
                h.set_confirmado(False)
                h.set_id_cliente(None)
                h.set_id_servico(None)
                h.set_id_profissional(id_profissional)
                HorarioDAO.inserir(h)

                hora += timedelta(minutes=intervalo)
            data_atual += timedelta(days=1)

    @staticmethod
    def visualizar_agenda(id_profissional):
        horarios = []
        for h in View.horario_filtrar_profissional(id_profissional):
            cliente = None
            servico = None
            if h.get_id_cliente():
                cliente = View.cliente_listar_id(h.get_id_cliente())
            if h.get_id_servico():
                servico = View.servico_listar_id(h.get_id_servico())

            horarios.append({
                "id": h.get_id(),
                "data": h.get_data(),
                "confirmado": h.get_confirmado(),
                "cliente": cliente.get_nome() if cliente else "—",
                "servico": servico.get_descricao() if servico else "—"
            })
        return horarios

    @staticmethod
    def visualizar_meus_servicos(id_cliente):
        servicos = []
        for h in View.horario_listar():
            if h.get_id_cliente() == id_cliente:
                profissional = View.profissional_listar_id(h.get_id_profissional())
                servico = View.servico_listar_id(h.get_id_servico())

                servicos.append({
                    "data": h.get_data(),
                    "confirmado": h.get_confirmado(),
                    "profissional": profissional.get_nome() if profissional else "—",
                    "servico": servico.get_descricao() if servico else "—"
                })
        servicos.sort(key=lambda s: s["data"])
        return servicos

    @staticmethod
    def confirmar_servico(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)


    @staticmethod
    def profissional_abrir_agenda(id_profissional, dias=7):
        agora = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        horarios_atuais = View.horario_filtrar_profissional(id_profissional)
        datas_existentes = [h.get_data().date() for h in horarios_atuais]

        for i in range(dias):
            dia = agora + timedelta(days=i)
            for hora in range(8, 16):
                data_hora = dia.replace(hour=hora)
                if data_hora.date() not in datas_existentes:
                    View.horario_inserir(
                        data=data_hora,
                        confirmado=False,
                        id_cliente=None,
                        id_servico=None,
                        id_profissional=id_profissional
                    )

    @staticmethod
    def profissional_visualizar_agenda(id_profissional):
        return [
            h for h in View.horario_listar()
            if h.get_id_profissional() == id_profissional
        ]
    
    @staticmethod
    def listar_agenda_profissional_ordenada(id_prof, ordem="asc"):
        lista = View.profissional_visualizar_agenda(id_prof)
        return sorted(
            lista,
            key=lambda h: h.get_data(),
            reverse=(ordem == "desc")
        )


    @staticmethod
    def profissional_confirmar_servico(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)

    @staticmethod
    def cliente_visualizar_servicos(id_cliente):
        return [
            h for h in View.horario_listar()
            if h.get_id_cliente() == id_cliente
        ]
    
    @staticmethod
    def listar_servicos_cliente_ordenado(id_cliente, ordem="asc"):
        lista = View.cliente_visualizar_servicos(id_cliente)
        return sorted(
            lista,
            key=lambda h: h.get_data(),
            reverse=(ordem == "desc")
        )
    
    @classmethod
    def avaliar_profissional(cls, id_prof, id_cliente, nota, comentario):
       ProfissionalDAO.abrir()  # garante que a lista está carregada

       prof = cls.profissional_listar_id(id_prof)
       if not prof:
        print(f"[ERRO] Profissional com id={id_prof} não encontrado.")
        return False


       prof.add_avaliacao(id_cliente, nota, comentario)

       lista = ProfissionalDAO.listar()
       atualizado = False

       for i, p in enumerate(lista):
        if p.get_id() == prof.get_id():
            lista[i] = prof
            atualizado = True
            break

       if not atualizado:
        print(f"[ERRO] Profissional {prof.get_nome()} não estava na lista do DAO.")
        return False

       ProfissionalDAO.salvar()
       return True

    @classmethod
    def listar_atendimentos_cliente(cls, id_cliente: int) -> List:
        return HorarioDAO.listar_agenda_cliente(id_cliente)

    @staticmethod
    def alterar_senha(id_usuario, nova_senha, tipo):
        if tipo == "c":
            c = View.cliente_listar_id(id_usuario)
            if c:
                if hasattr(c, "set_senha"):
                    c.set_senha(nova_senha)
                    ClienteDAO.atualizar(c)
                elif isinstance(c, dict):
                    c_key = c.get("id") or c.get("_Cliente__id")
                    lista = ClienteDAO.listar()
                    for item in lista:
                        if (isinstance(item, dict) and (item.get("id") == c_key or item.get("_Cliente__id") == c_key)) \
                           or (hasattr(item, "get_id") and item.get_id() == c_key):
                            if hasattr(item, "set_senha"):
                                item.set_senha(nova_senha)
                                ClienteDAO.atualizar(item)
                            else:
                                item["senha"] = nova_senha
                                try:
                                    ClienteDAO.salvar(lista)
                                except Exception:
                                    pass
                            return True
                return True
            return False

        elif tipo == "p":
            p = View.profissional_listar_id(id_usuario)
            if p:
                if hasattr(p, "set_senha"):
                    p.set_senha(nova_senha)
                    ProfissionalDAO.atualizar(p)
                else:
                    lista = ProfissionalDAO.listar()
                    for item in lista:
                        if (isinstance(item, dict) and (item.get("id") == id_usuario or item.get("_Profissional__id") == id_usuario)) \
                           or (hasattr(item, "get_id") and item.get_id() == id_usuario):
                            if hasattr(item, "set_senha"):
                                item.set_senha(nova_senha)
                                ProfissionalDAO.atualizar(item)
                            else:
                                item["senha"] = nova_senha
                                try:
                                    ProfissionalDAO.salvar(lista)
                                except Exception:
                                    pass
                            return True
                return True
            return False

        elif tipo == "a":
    # Garante que o admin exista
          View.cliente_criar_admin()
          lista = ClienteDAO.listar()
          for c in lista:
            if hasattr(c, "get_email") and c.get_email() == "admin":
              c.set_senha(nova_senha)
              ClienteDAO.atualizar(c)
              ClienteDAO.salvar()  # ✅ garante gravação imediata
              return True
            elif isinstance(c, dict) and (c.get("email") == "admin" or c.get("_Cliente__email") == "admin"):
              c["senha"] = nova_senha
              try:
                ClienteDAO.salvar(lista)
              except Exception:
                pass
              return True
          return False
