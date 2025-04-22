def maior(x, y, z):
    return max(x, y, z)

num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
num3 = float(input("Digite o terceiro número: "))
resultado = maior(num1, num2, num3)
print(f"O maior valor é: {resultado}")