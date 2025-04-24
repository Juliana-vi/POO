valores = [int(input()) for _ in range(100)]
maior_valor = max(valores)
posicao = valores.index(maior_valor) + 1
print(maior_valor)
print(posicao)