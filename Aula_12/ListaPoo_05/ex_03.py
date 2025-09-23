from datetime import datetime

class Contato:
    def __init__(self, id: int, nome: str, email: str, fone: str, nascimento: datetime):
        self._id = id
        self._nome = nome
        self._email = email
        self._fone = fone
        self._nascimento = nascimento

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def get_fone(self):
        return self._fone

    def get_nascimento(self):
        return self._nascimento

    def set_nome(self, nome):
        self._nome = nome

    def set_email(self, email):
        self._email = email

    def set_fone(self, fone):
        self._fone = fone

    def set_nascimento(self, nascimento):
        self._nascimento = nascimento

    def ToString(self):
        return (f"ID: {self._id}\n"
                f"Nome: {self._nome}\n"
                f"E-mail: {self._email}\n"
                f"Telefone: {self._fone}\n"
                f"Nascimento: {self._nascimento.strftime('%d/%m/%Y')}\n")

class ContatoUI:
    contatos = []

    @staticmethod
    def Main():
        while True:
            opcao = ContatoUI.Menu()
            if opcao == 1:
                ContatoUI.Inserir()
            elif opcao == 2:
                ContatoUI.Listar()
            elif opcao == 3:
                ContatoUI.Atualizar()
            elif opcao == 4:
                ContatoUI.Excluir()
            elif opcao == 5:
                ContatoUI.Pesquisar()
            elif opcao == 6:
                ContatoUI.Aniversariantes()
            elif opcao == 7:
                print("Saindo da agenda")
                break
            else:
                print("Opção inválida")

    @staticmethod
    def Menu():
        print("\n--- Agenda de Contatos ---")
        print("1. Inserir novo contato")
        print("2. Listar contatos")
        print("3. Atualizar contato")
        print("4. Excluir contato")
        print("5. Pesquisar contato pelas iniciais")
        print("6. Aniversariantes do mês")
        print("7. Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def Inserir():
        try:
            id = int(input("ID: "))
            nome = input("Nome: ")
            email = input("E-mail: ")
            fone = input("Telefone: ")
            nasc_str = input("Nascimento (dd/mm/aaaa): ")
            nascimento = datetime.strptime(nasc_str, "%d/%m/%Y")
            contato = Contato(id, nome, email, fone, nascimento)
            ContatoUI.contatos.append(contato)
            print("Contato inserido com sucesso")
        except Exception as e:
            print(f"Erro ao inserir contato: {e}")

    @staticmethod
    def Listar():
        if not ContatoUI.contatos:
            print("Nenhum contato cadastrado.")
        else:
            for contato in ContatoUI.contatos:
                print(contato.ToString())

    @staticmethod
    def Atualizar():
        try:
            id = int(input("Informe o ID do contato a atualizar: "))
            contato = next((c for c in ContatoUI.contatos if c.get_id() == id), None)
            if contato:
                nome = input(f"Novo nome ({contato.get_nome()}): ") or contato.get_nome()
                email = input(f"Novo e-mail ({contato.get_email()}): ") or contato.get_email()
                fone = input(f"Novo telefone ({contato.get_fone()}): ") or contato.get_fone()
                nasc_str = input(f"Nova data de nascimento ({contato.get_nascimento().strftime('%d/%m/%Y')}): ")
                nascimento = contato.get_nascimento()
                if nasc_str:
                    nascimento = datetime.strptime(nasc_str, "%d/%m/%Y")
                contato.set_nome(nome)
                contato.set_email(email)
                contato.set_fone(fone)
                contato.set_nascimento(nascimento)
                print("Contato atualizado com sucesso")
            else:
                print("Contato não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar contato: {e}")

    @staticmethod
    def Excluir():
        try:
            id = int(input("Informe o ID do contato a excluir: "))
            contato = next((c for c in ContatoUI.contatos if c.get_id() == id), None)
            if contato:
                ContatoUI.contatos.remove(contato)
                print("Contato excluído com sucesso")
            else:
                print("Contato não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir contato: {e}")

    @staticmethod
    def Pesquisar():
        iniciais = input("Informe as iniciais do nome: ").lower()
        encontrados = [c for c in ContatoUI.contatos if c.get_nome().lower().startswith(iniciais)]
        if encontrados:
            for contato in encontrados:
                print(contato.ToString())
        else:
            print("Nenhum contato encontrado com essas iniciais.")

    @staticmethod
    def Aniversariantes():
        try:
            mes = int(input("Informe o mês (1-12): "))
            aniversariantes = [c for c in ContatoUI.contatos if c.get_nascimento().month == mes]
            if aniversariantes:
                print(f"Contatos que fazem aniversário em {mes}:")
                for contato in aniversariantes:
                    print(contato.ToString())
            else:
                print("Nenhum aniversariante neste mês.")
        except Exception as e:
            print(f"Erro ao buscar aniversariantes: {e}")

if __name__ == "__main__":
    ContatoUI.Main()