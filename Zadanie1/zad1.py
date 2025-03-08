import math


def factorial(n):
    """Oblicza silnię liczby n"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def normalize_angle(x, radians):
    """Sprowadza kąt do przedziału 0..2π"""
    if not radians:
        x = math.radians(x)  # Konwersja stopni na radiany
    x = x % (2 * math.pi)  # Redukcja do zakresu 0..2π

    if x > math.pi:  # 2. ćwiartka
        x -= math.pi
    elif x > math.pi / 2:  # 3. ćwiartka
        x = math.pi - x
    elif x > 3 * math.pi / 2:  # 4. ćwiartka
        x = 2 * math.pi - x

    return x


def sin_taylor(arg, n, radians=False):
    """Oblicza sinus z rozwinięcia Taylora"""
    x = normalize_angle(arg, radians)  # Sprowadzenie kąta do 0..2π
    fun = 0  # Przybliżenie funkcji sinus

    # Nagłówek tabeli
    print(
        f"{'Iteracja':<10}{'Wyraz szeregu':<20}{'Przybliżenie sin(x)':<30}{'math.sin(x)':<20}{'Bezwzględna różnica':<20}")
    print("=" * 120)

    for j in range(n):
        power = 2 * j + 1  # Kolejne wykładniki: 1, 3, 5, 7, ...
        term = (-1) ** j * (x ** power) / factorial(power)  # Wyraz szeregu
        fun += term  # Suma wyrazów szeregu

        # Obliczenie wartości referencyjnej
        true_sin = math.sin(math.radians(arg) if not radians else arg)
        abs_error = abs(fun - true_sin)

        # Wypisanie wyników
        print(f"{j + 1:<10}{term:<20.6f}{fun:<30.6f}{true_sin:<20.6f}{abs_error:<20.6f}")

    return fun


# Testowanie dla kąta 200 stopni (powinno działać poprawnie dla pełnego zakresu)
sin_taylor(200, 10, radians=False)
