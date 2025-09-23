from datetime import datetime
from enum import Enum

class Pagamento(Enum):
    EmAberto = 1
    PagoParcial = 2
    Pago = 3

class Boleto:
    def __init__(self, codBarras: str, dateEmissao: datetime, dataVencimento: datetime, valorBoleto: float):
        self._codBarras = codBarras
        self._dateEmissao = dateEmissao
        self._dataVencimento = dataVencimento
        self._valorBoleto = valorBoleto
        self._valorPago = 0.0
        self._dataPagto = None
        self._situacaoPagamento = Pagamento.EmAberto

    def get_codBarras(self):
        return self._codBarras

    def get_dateEmissao(self):
        return self._dateEmissao

    def get_dataVencimento(self):
        return self._dataVencimento

    def get_valorBoleto(self):
        return self._valorBoleto

    def get_valorPago(self):
        return self._valorPago

    def get_dataPagto(self):
        return self._dataPagto

    def get_situacaoPagamento(self):
        return self._situacaoPagamento

    def set_codBarras(self, codBarras):
        self._codBarras = codBarras

    def set_dateEmissao(self, dateEmissao):
        self._dateEmissao = dateEmissao

    def set_dataVencimento(self, dataVencimento):
        self._dataVencimento = dataVencimento

    def set_valorBoleto(self, valorBoleto):
        self._valorBoleto = valorBoleto

    def set_valorPago(self, valorPago):
        self._valorPago = valorPago

    def set_dataPagto(self, dataPagto):
        self._dataPagto = dataPagto

    def set_situacaoPagamento(self, situacaoPagamento):
        self._situacaoPagamento = situacaoPagamento

    def Pagar(self, valorPago: float):
        if valorPago <= 0:
            print("Valor pago deve ser maior que zero.")
            return
        self._valorPago += valorPago
        self._dataPagto = datetime.now()
        self._situacaoPagamento = self.Situacao()

    def Situacao(self):
        if self._valorPago == 0:
            return Pagamento.EmAberto
        elif self._valorPago < self._valorBoleto:
            return Pagamento.PagoParcial
        else:
            return Pagamento.Pago

    def ToString(self):
        return (f"Código de Barras: {self._codBarras}\n"
                f"Data de Emissão: {self._dateEmissao.strftime('%d/%m/%Y')}\n"
                f"Data de Vencimento: {self._dataVencimento.strftime('%d/%m/%Y')}\n"
                f"Valor do Boleto: R$ {self._valorBoleto:.2f}\n"
                f"Valor Pago: R$ {self._valorPago:.2f}\n"
                f"Data do Pagamento: {self._dataPagto.strftime('%d/%m/%Y %H:%M:%S') if self._dataPagto else '---'}\n"
                f"Situação: {self._situacaoPagamento.name}")

if __name__ == "__main__":
    cod = input("Código de Barras: ")
    emissao_str = input("Data de Emissão (dd/mm/aaaa): ")
    venc_str = input("Data de Vencimento (dd/mm/aaaa): ")
    valor = float(input("Valor do Boleto: "))
    dateEmissao = datetime.strptime(emissao_str, "%d/%m/%Y")
    dataVencimento = datetime.strptime(venc_str, "%d/%m/%Y")
    boleto = Boleto(cod, dateEmissao, dataVencimento, valor)
    print("\nDados do boleto:")
    print(boleto.ToString())

    while True:
        pagar = input("\nDeseja pagar o boleto? (s/n): ")
        if pagar.lower() == 's':
            valorPago = float(input("Valor a pagar: "))
            boleto.Pagar(valorPago)
            print("\nDados do boleto após pagamento:")
            print(boleto.ToString())
            if boleto.get_situacaoPagamento() == Pagamento.Pago:
                print("Boleto totalmente pago")
                break
        else:
            break