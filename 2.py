sec = int(input("Enter time in seconds: "))
hour = sec // 3600
m = sec % 3600 // 60
s = sec % 3600 % 60

if 10 > hour >= 0:
    if 10 > m >= 0:
        if 10 > s >= 0:
            print(f"0{hour}:0{m}:0{s}")
        else:
            print(f"0{hour}:0{m}:{s}")
    else:
        print(f"0{hour}:{m}:{s}")

if hour >= 10:
    if 10 > m >= 0:
        if 10 > s >= 0:
            print(f"{hour}:0{m}:0{s}")
        else:
            print(f"{hour}:0{m}:{s}")
    else:
        print(f"{hour}:{m}:{s}")
