sec = int(input("Enter time in seconds: "))
hour = sec // 3600
print(hour)
m = sec % 3600 // 60
print(m)
s = sec % 3600 % 60
print(s)