import math

class Circulo:
    def __init__(self, raio):
        self.raio = raio

    def calcular_area(self):
        return math.pi * (self.raio ** 2)

    def calcular_circunferencia(self):
        return 2 * math.pi * self.raio

def main():
    raio = float(input("Digite o raio do círculo: "))

    circulo = Circulo(raio)

    area = circulo.calcular_area()
    circunferencia = circulo.calcular_circunferencia()

    print(f"A área do círculo é: {area:.2f}")
    print(f"A circunferência do círculo é: {circunferencia:.2f}")

if __name__ == "__main__":
    main()