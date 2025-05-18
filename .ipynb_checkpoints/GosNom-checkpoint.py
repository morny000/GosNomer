import re

def analyze_license_plate(license_plate):
    """
    Анализирует российский автомобильный номер и возвращает список признаков, включая проверку "блатных" номеров по регионам.

    Args:
        license_plate: Строка с автомобильным номером (например, "А123ВГ77").

    Returns:
        Словарь с признаками номера.
    """

    features = {}

    # 1. Базовая проверка формата
    if not re.match(r"^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$", license_plate):
        features['valid_format'] = False
        return features
    else:
        features['valid_format'] = True

    # Разделение номера на части
    letter1 = license_plate[0]
    digits = license_plate[1:4]
    letter2 = license_plate[4:6]
    region = license_plate[6:]

    features['letter1'] = letter1
    features['digits'] = digits
    features['letter2'] = letter2
    features['region'] = region

    # 2. Характеристики номера

    # 2.1 Тип номера (пока упрощенно, только стандартный)
    features['type'] = "Стандартный"

    # 2.2 Буквенные комбинации
    letters = letter1 + letter2
    features['letters'] = letters

    #Зеркальные буквы
    features["letters_is_mirror"] = letter2[0] == letter1 if len(letter2) == 2 else False

    # Повторяющиеся буквы
    features['repeated_letters'] = len(set(letter2)) == 1 if len(letter2) == 2 else False
    features['triple_letters'] = letter1 == letter2[0] and letter1 == letter2[1] if len(letter2) == 2 else False


    # 2.3 Цифровые комбинации
    features['is_mirror_digits'] = digits[0] == digits[2]
    features['is_round_digits'] = digits in ("100", "200", "300", "400", "500", "600", "700", "800", "900")
    features['repeated_digits'] = len(set(digits)) == 1
    features['ascending_digits'] = digits == ''.join(map(str, range(int(digits[0]), int(digits[0]) + 3)))
    features['descending_digits'] = digits == ''.join(map(str, range(int(digits[0]), int(digits[0]) - 3, -1)))

    #чередующийся порядок цифр
    features["alternating_digits"] = digits[0] == digits[2] and digits[1] != digits[0]

    features['sum_of_digits'] = sum(int(d) for d in digits)
    features['even_digits'] = sum(1 for d in digits if int(d) % 2 == 0)
    features['odd_digits'] = sum(1 for d in digits if int(d) % 2 != 0)
    features['has_7'] = '7' in digits
    features['has_8'] = '8' in digits


    happy_numbers = ['777', '888', '007']
    features['is_happy_number'] = digits in happy_numbers



    features['region'] = region


    features["digits_match_region"] = digits == region if len(region) == 3 else False

    prestigious_regions = ["77", "99", "199", "777", "78", "98"]
    features["is_prestigious_region"] = region in prestigious_regions


    prestigious_letters = ['А', 'М', 'В', 'О', 'Р', 'С']
    letter_prestige = 0
    if letter1 in prestigious_letters:
        letter_prestige += 1
    for letter in letter2:
        if letter in prestigious_letters:
            letter_prestige += 1
    features['letter_prestige'] = letter_prestige


    even_count = sum(1 for digit in digits if int(digit) % 2 == 0)
    odd_count = 3 - even_count
    features["even_digit_count"] = even_count
    features["odd_digit_count"] = odd_count


    blat_series = {
        "77": ["ЕКХ", "ККХ", "САС", "АМР", "АММ", "ССС", "ККК", "ООО", "*ММ", "КММ", "ММР", "РМР", "АМ0", "К00"], #Москва
        "99": ["ЕКХ", "АММ", "ССС", "ККК"], #Москва
        "97": ["ЕКХ", "ССС"],#Москва
        "50": ["AM", "BM", "КМО", "CM", "ОМО", "MM", "TM", "HM", "УМО", "ХM", "AMM", "MMM"], #Московская область
        "90": ["AMM", "MMM"], #Московская область
        "78": ["OB", "OTT", "OMM", "00M", "OPP", "OOH", "OA", "AAA", "000", "OKC", "00C", "BBB", "MMM", "OCX"], #Санкт-Петербург
        "98": ["OB", "OTT", "OMM", "00M", "OPP", "OOH", "OA", "AAA", "000", "OKC", "00C", "BBB", "MMM", "OCX"], #Санкт-Петербург
        "04": ["XXX", "TTT", "PPP", "PPA", "MPA", "000", "HHH", "CCC"],#Республика Алтай
        "02": ["PKC", "KKC", "000", "AAA"],#Республика Башкортостан
        "10": ["TTT", "HHH", "MMM", "EMP", "CCC", "000"], #Республика Карелия
        "11": ["TTT", "PPP", "AAA"],#Республика Коми
        "ММ": ["*ММ", "KM"], #Республика Татарстан
        "23": ["PPP", "HHH", "000", "ККК"],#Краснодарский край
        "24": ["КРК", "000", "МКК"],#Красноярский край
        "25": ["В00", "ААА", "ААА1", "ННН", "МММ", "ССС", "ХХХ", "000", "ТТТ", "MBK", "BOO", "НОО", "УОО", "СОО"],#Приморский край
        "125":["ААА"],#Приморский край
        "34": ["AAM", "PAA", "AAA", "ACK", "УУУ", "AAK"],#Волгоградская область
        "36": ["AAA", "BOA", "МММ", "AАК", "ККК", "РРР"],#Воронежская область
        "40": ["МАА", "000", "TTT", "PPP"],#Калужская область
        "45": ["000", "TTT", "ОКО"],#Курганская область
        "54": ["ACK", "АНО", "AАО", "PPP", "МОР"],#Новосибирская область
        "57": ["AAA", "AОО", "МАА", "MMMOBД", "ОАО"],#Орловская область
        "61": ["APO", "AAA", "АРУ", "KKK", "HHH", "MMM", "000", "BBK"],#Ростовская область
        "64": ["AAA", "PPP", "XXX", "МММ", "ОАА"],#Саратовская область
        "70": ["АТО"],#Томская область
        "72": ["РТО", "АТО", "МТО", "НТО"],#Тюменская область
        "76": ["УТО", "ВАА", "ВОА", "ККК"],#Ярославская область
        "29": ["TTT", "PPP", "МАО"],#Архангельская область
        "62": ["С62", "М62", "Х62", "АРО"],#Рязанская область
        "63": ["PAA", "AAP"],#Самарская область
        "любые регионы": ["ООО", "ААА", "МММ", "ВВВ", "ЕЕЕ", "ККК", "ННН", "РРР", "ССС", "ТТТ", "УУУ", "ХХХ",
                         "АМР", "АМО", "КММ", "МВМ", "СВВ", "ЕКХ", "САС", "ММВ", "ВМВ", "ВМР", "КМР", "НМР",
                         "АУЕ", "УМР", "КРУ", "ВРУ", "СРУ", "ЕРУ", "ХАМ", "МУР", "НЛО", "АУУ", "ВАО", "ЕАО",
                         "КАО", "МАО", "НАО", "РАО", "САО", "ТАО", "УАО", "ХАО", "КОТ", "ВОХ", "МОР", "ТОР",
                         "ХУМ", "ЕМА",  "ЕКЛ", "АВМ", "ВММ", "МВК", "НВВ", "КВВ"]
    }

    features["is_blatnoy"] = False

    if region in blat_series:
        for series in blat_series[region]:


            if series == letters:
                features["is_blatnoy"] = True
                break


            if len(series) == 3 and (letter1 + digits[:2]) == series[:3]:
               features["is_blatnoy"] = True
               break

            if len(series) == 3 and digits == "000" and letter1 == series[0]:
                 features["is_blatnoy"] = True
                 break


    return features


license_plate = input("Введите номер автомобиля (например, А123ВГ77): ")
analysis = analyze_license_plate(license_plate)

print("\nРезультаты анализа:")
for key, value in analysis.items():
    print(f"{key}: {value}")