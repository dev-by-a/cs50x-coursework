number = str(int(input("Number: ")))
total = 0
for i, digit in enumerate(reversed(number)):
    d = int(digit)
    if i % 2 == 1: # every other digit from second-to-last
        d *= 2
        if d > 9:
            d -= 9
    total += d

length = len(number)
first_two = number[:2]
first_one = number[0]

if total % 10 == 0:
    if length == 15 and first_two in ["34", "37"]:
        print("AMEX")
    elif length == 16 and first_two in ["51", "52", "53", "54", "55"]:
        print("MASTERCARD")
    elif first_one == "4" and length in [13, 16]:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
    
