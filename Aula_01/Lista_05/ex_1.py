def maior(x, y):
    return x if x > y else y

num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
resultado = maior(num1, num2)
print(f"O maior valor é: {resultado}")