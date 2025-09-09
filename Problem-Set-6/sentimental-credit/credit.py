import re
list_digit = []
sum = 0


def main():
    while True:
        try:
            n = input("Number: ")
            match = re.match(r"^\d*$", n)
            if not match:
                continue
            else:
                sum = value(n)
                if sum == 0:
                    card(n)
                    break
                else:
                    print("INVALID")
                    break
        except ValueError:
            continue


def value(n):
    reverse = n[::-1]

    for i in range(1, len(reverse), 2):
        last_digit_start = reverse[i]
        list_digit.append(int(last_digit_start))

    squ = square(list_digit)
    addition(squ)
    sum = valid_check(n)
    return sum


def square(n):
    str_dig = ""
    for i in range(0, len(n)):
        squ = n[i] * 2
        str_dig += str(squ)
    return str_dig


def addition(n):
    global sum
    for add in n:
        add = int(add)
        sum = sum + add


def valid_check(n):
    global sum
    reverse = n[::-1]

    for i in range(0, len(reverse), 2):
        last_digit_start = reverse[i]
        digit = int(last_digit_start)
        sum = sum + digit
    return sum % 10


def card(c):
    if match := re.match(r"^[0-3][4-7]\d{13}$", c):
        print("AMEX")
    elif match := re.match(r"^([5][1-5])\d{14}$", c):
        print("MASTERCARD")
    elif match := re.match(r"^([4])(\d{12}|\d{13}|\d{14}|\d{15})$", c):
        print("VISA")
    else:
        print("INVALID")


main()
