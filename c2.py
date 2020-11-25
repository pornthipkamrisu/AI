money = int(input("Net income : "))
tax = 0
if money <= 0:
    print("Wrong input : negative income.")
else:
    if money <= 150000:
        money = money
        tax = 0
    elif money <= 300000:
        money = money - 150000
        tax = (money * 0.05)
    elif money <= 500000:
        money = money - 300000
        tax = ((money * 0.1) + 75000)
    elif money <= 750000:
        money = money - 500000
        tax = ((money * 0.15) + 27500)
    elif money <= 1000000:
        money = money - 750000
        tax = ((money * 0.2) + 65000)
    elif money <= 2000000:
        money = money - 1000000
        tax = ((money * 0.25) + 115000)
    elif money <= 5000000:
        money = money - 2000000
        tax = ((money * 0.3) + 365000)
    else:
        money = money - 5000000
        tax = ((money * 0.35) + 1265000)
print("Your income tax : ", tax)