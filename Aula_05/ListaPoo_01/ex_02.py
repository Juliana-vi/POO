class Viagem:
    def __init__(self, distancia_km, horas, min):
        self.distancia_km = distancia_km
        self.horas = horas
        self.min = min

    def calcular_velocidade_media(self):
        tempo_total_horas = self.horas + self.min / 60
        if tempo_total_horas == 0:
            return 0
        return self.distancia_km / tempo_total_horas

def main():
    distancia = float(input("Digite a distância da viagem em km: "))
    horas = int(input("Digite o tempo gasto em horas: "))
    min = int(input("Digite o tempo gasto em minutos: "))

    viagem = Viagem(distancia, horas, min)

    velocidade_media = viagem.calcular_velocidade_media()
    print(f"A velocidade média da viagem foi de {velocidade_media:.2f} km/h")

if __name__ == "__main__":
    main()