import math
pi = 3.141592653589
liczba = input(f'''Wprowadz liczbe w stopniach lub radianach dodając na końcu stosowną literkę
    r - radiany(np 0.5236r)
    s - stopnie(np 90s)
    ''')



def factorial(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
def wielomianTaylora(wartosc,znak,potega):
    return znak*(wartosc**potega) / factorial(potega)

def normalize_angle(x):
    x = abs(x) % (2 * math.pi) if math.radians else abs(math.radians(x)) % (2 * math.pi)
    return x if x <= math.pi else 2 * math.pi - x

def sinus(val):
    val = normalize_angle(val)

    suma = val
    znak = -1.0
    potega = 3

    print("\nKolejne wyrazy szeregu Taylora:")
    print(
        f"{'Iteracja':<10}{'Wyraz szeregu':<20}{'Przybliżenie sin(x)':<30}{'math.sin(x)':<20}{'Bezwzględna różnica':<20}")
    print("=" * 120)

    for i in range(1, 11):  # Iteracja po 10 wyrazach szeregu
        wyraz = wielomianTaylora(val, znak, potega)
        suma += wyraz
        print(f"{i:<10}{wyraz:<20.10f}{suma:<30.10f}{math.sin(val):<20.10f}{abs(suma - math.sin(val)):<20.10f}")

        znak *= -1
        potega += 2


    return suma

def oblicz_sinus(x, czy_stopnie):

    if czy_stopnie:
        x = math.radians(float(x))

    sin_z_biblioteki = math.sin(x)
    sin_liczony = sinus(x)
    roznica = abs(sin_liczony - sin_z_biblioteki)

    print(f"Z iblioteka: {sin_z_biblioteki}")
    print(f"Ręcznie: {sin_liczony}")
    print(f"Różnica: {roznica}")

num= float(liczba[:-1]) if '.' in liczba and liczba[-1]=='r' else int(liczba[:-1])
oblicz_sinus(num,czy_stopnie= True if liczba[-1].lower()=='s' else False)