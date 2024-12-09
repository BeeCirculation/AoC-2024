with open("input.txt", "r") as file:
    text = "".join(file.readlines())

#text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
max_digit_length = 3
start = 0
valid = True
total = 0
on = True
while "mul(" in text[start:]:
    valid = True
    index = text.find("mul(", start) + 4
    do_index = text.find("do()", start, index)
    dont_index = text.find("don't()", start, index)

    if do_index < index and do_index != -1:
        on = True
    if dont_index < index and dont_index > do_index and dont_index != -1:
        on = False

    num1 = ""
    i = 0
    while text[index + i].isnumeric():
        if len(num1) > max_digit_length:
            valid = False
            break
        num1 += text[index + i]
        i += 1
    try:
        num1 = int(num1)
    except:
        valid = False

    index += i + 1

    if text[index - 1] != ",":
        valid = False

    num2 = ""
    i = 0
    while text[index + i].isnumeric():
        if len(num2) > max_digit_length:
            valid = False
            break
        num2 += text[index + i]
        i += 1
    try:
        num2 = int(num2)
    except:
        valid = False

    index += i

    if text[index] != ")":
        valid = False

    if valid and on:
        total += num1 * num2
    #print(total)

    start = index

print(total)

