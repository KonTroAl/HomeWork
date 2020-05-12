a = int(input("Введите целое положительное число: "))
b = 0
while a > 0:
    c = a % 10
    a //= 10
    if c >= b:
        b = c
print(b)
