Number = input("Please enter 3 integers : ")
num1 = int(Number[0])
num2 = int(Number[2])
num3 = int(Number[4])
if ((num1 > num2) and (num1 > num3) and (num2 > num3)):
    Max = num1
    Min = num3
elif ((num2 > num1) and (num2 > num3) and (num1 > num3)):
    Max = num2
    Min = num3
elif ((num1 > num2) and (num1 > num3) and (num3 > num2)):
    Max = num1
    Min = num2
elif ((num2 > num1) and (num2 > num3) and (num3 > num1)):
    Max = num2
    Min = num1
elif ((num3 > num2) and (num3 > num2) and (num2 > num1)):
    Max = num3
    Min = num1
elif ((num3 > num2) and (num3 > num1) and (num1 > num2)):
    Max = num3
    Min = num1
else:
    pass
print("Max is", Max)
print("Min is", Min)