from datetime import datetime

class Paciente:
    def __init__(self, nome: str, cpf: str, telefone: str, nascimento: datetime):
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone
        self._nascimento = nascimento

    def get_nome(self):
        return self._nome

    def get_cpf(self):
        return self._cpf

    def get_telefone(self):
        return self._telefone

    def get_nascimento(self):
        return self._nascimento

    def set_nome(self, nome):
        self._nome = nome

    def set_cpf(self, cpf):
        self._cpf = cpf

    def set_telefone(self, telefone):
        self._telefone = telefone

    def set_nascimento(self, nascimento):
        self._nascimento = nascimento

    def Idade(self):
        hoje = datetime.now()
        anos = hoje.year - self._nascimento.year
        meses = hoje.month - self._nascimento.month
        if hoje.day < self._nascimento.day:
            meses -= 1
        if meses < 0:
            anos -= 1
            meses += 12
        return f"{anos} anos e {meses} meses"

    def ToString(self):
        return (f"Nome: {self._nome}\n"
                f"CPF: {self._cpf}\n"
                f"Telefone: {self._telefone}\n"
                f"Nascimento: {self._nascimento.strftime('%d/%m/%Y')}\n"
                f"Idade: {self.Idade()}")

if __name__ == "__main__":
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    nasc_str = input("Data de nascimento (dd/mm/aaaa): ")
    nascimento = datetime.strptime(nasc_str, "%d/%m/%Y")
    paciente = Paciente(nome, cpf, telefone, nascimento)
    print("\nDados do paciente:")
    print(paciente.ToString())