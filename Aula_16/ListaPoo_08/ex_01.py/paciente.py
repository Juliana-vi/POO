from datetime import datetime

class Paciente:
    def __init__(self,nome,cpf,fone,nasc):
        self.nome = nome
        self.cpf = cpf
        self.fone = fone
        self.nasc = nasc
        self.idade = self.calc_idade()
    def calc_idade(self):
        nasc_dt = datetime.strptime(self.nasc, "%d/%m/%Y")
        hoje = datetime.today()
        idade = hoje.year - nasc_dt.year - ((hoje.month, hoje.day) < (nasc_dt.month, nasc_dt.day))
        return idade
    def __str__(self):
        return f"Idade = {self.calc_idade()}"
