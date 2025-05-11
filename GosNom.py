import re

def analyze(nomer):
    f = {}

    if not re.match(r"^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$", nomer):
        f['valid_format'] = False
        return f
    else:
        f['valid_format'] = True

    letter1 = nomer[0]
    digits = nomer[1:4]
    letter2 = nomer[4:6]
    region = nomer[6:]

    f['letter1'] = letter1
    f['digits'] = digits
    f['letter2'] = letter2
    f['region'] = region


    f['type'] = "Стандартный"



    letters = letter1 + letter2
    f['letters'] = letters

    f["letters_is_mirror"] = letter2[0] == letter1 if len(letter2) == 2 else False

    f['repeated_letters'] = len(set(letter2)) == 1 if len(letter2) == 2 else False
    f['triple_letters'] = letter1 == letter2[0] and letter1 == letter2[1] if len(letter2) == 2 else False


    f['is_mirror_digits'] = digits == digits[::-1]
    f['is_round_digits'] = digits in ("100", "200", "300", "400", "500", "600", "700", "800", "900")
    f['repeated_digits'] = len(set(digits)) == 1
    f['ascending_digits'] = digits == ''.join(map(str, range(int(digits[0]), int(digits[0]) + 3)))
    f['descending_digits'] = digits == ''.join(map(str, range(int(digits[0]), int(digits[0]) - 3, -1)))

    f["alternating_digits"] = digits[0] == digits[2] and digits[1] != digits[0]

    f['sum_of_digits'] = sum(int(d) for d in digits)
    f['even_digits'] = sum(1 for d in digits if int(d) % 2 == 0)
    f['odd_digits'] = sum(1 for d in digits if int(d) % 2 != 0)
    f['есть 7'] = '7' in digits
    f['есть 8'] = '8' in digits

    happy_numbers = ['777', '888', '007']
    f['lucky number'] = digits in happy_numbers


    f['region'] = region

    f["digits_match_region"] = digits == region if len(region) == 3 else False
    prestigious_regions = ["77", "99", "199", "777", "78", "98"]
    f["pristish"] = region in prestigious_regions

    prestigious_letters = ['А','М','В','О','Р','С']
    letter_prestige = 0
    if letter1 in prestigious_letters:
        letter_prestige += 1
    for letter in letter2:
        if letter in prestigious_letters:
            letter_prestige += 1
    f['pristish letter'0] = letter_prestige

    even_count = sum(1 for digit in digits if int(digit) % 2 == 0)
    odd_count = 3 - even_count
    f["even_digit_count"] = even_count
    f["odd_digit_count"] = odd_count

    return f

nomer = input("Введите номер автомобиля (например, А123ВГ77): ")
analysis = analyze(nomer)

print("\nРезультаты анализа:")
for key, value in analysis.items():
    print(f"{key}: {value}")