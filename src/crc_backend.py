import random


def text_to_binary(text):
    """
    Zamienia tekst na binarną reprezentację (ciąg 0 i 1).
    """
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    """
    Zamienia binarną reprezentację na tekst.
    """
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


def crc_encode(data, polynomial):
    """
    Oblicza CRC dla dowolnego tekstu przy użyciu zadanego wielomianu.
    """
    data_binary = text_to_binary(data)  # Zamiana tekstu na binarny ciąg
    data_bits = list(data_binary)
    poly_bits = list(polynomial)
    data_bits.extend(['0'] * (len(poly_bits) - 1))  # Dodanie bitów zerowych

    for i in range(len(data_bits) - len(poly_bits) + 1):
        if data_bits[i] == '1':
            for j in range(len(poly_bits)):
                data_bits[i + j] = str(int(data_bits[i + j] != poly_bits[j]))

    remainder = ''.join(data_bits[-(len(poly_bits) - 1):])  # Reszta CRC
    return data_binary + remainder  # Dołączenie reszty CRC do oryginalnego ciągu


def highlight_errors(message, errors):
    """
    Zaznacza błędne bity w wiadomości. Poprawione bity są zaznaczone na zielono.
    """
    highlighted = ""
    for i, bit in enumerate(message):
        if i in errors:
            highlighted += f'<span style="color: red; font-weight: bold;">{bit}</span>'
        else:
            highlighted += bit
    return highlighted


#! TEMPORARY
def highlight_corrected(message, corrected):
    """
    Zaznacza błędne bity w wiadomości Poprawione bity są zaznaczone na zielono.
    """
    highlighted = ""
    for i, bit in enumerate(message):
        if i in corrected:
            highlighted += f'<span style="color: #03fc17; font-weight: bold;">{bit}</span>'
        else:
            highlighted += bit
    return highlighted


def introduce_error(message, error_rate):
    """
    Wprowadza błędy do wiadomości z zadaną częstością (error_rate).
    """
    message = list(message)
    for i in range(len(message)):
        if random.random() < error_rate:
            message[i] = '1' if message[i] == '0' else '0'
    return ''.join(message)


def crc_validate(received_data, polynomial):
    """
    Sprawdza wiadomość z kodem CRC i zwraca indeksy błędnych bitów.
    """
    data = list(received_data)
    poly = list(polynomial)
    # Oblicz CRC na podstawie danych wejściowych
    encoded_data = data[:]
    encoded_data.extend(['0'] * (len(poly) - 1))
    for i in range(len(encoded_data) - len(poly) + 1):
        if encoded_data[i] == '1':
            for j in range(len(poly)):
                encoded_data[i + j] = str(int(encoded_data[i + j] != poly[j]))

    # Zwracaj miejsca, w których występuje błąd
    remainder = ''.join(encoded_data[-(len(poly) - 1):])
    errors = [i for i, bit in enumerate(remainder) if bit != '0']
    print(f"Validation errors at positions: {errors}")  # Debug print
    return errors


def crc_correct(received_data, polynomial):
    """
    Poprawia błędy bitowe w binarnym kodzie po obliczeniu CRC.
    """
    data = list(received_data)
    poly = list(polynomial)
    # Oblicz CRC na podstawie danych wejściowych
    encoded_data = data[:]
    encoded_data.extend(['0'] * (len(poly) - 1))
    for i in range(len(encoded_data) - len(poly) + 1):
        if encoded_data[i] == '1':
            for j in range(len(poly)):
                encoded_data[i + j] = str(int(encoded_data[i + j] != poly[j]))

    # Znajdź miejsca, w których występuje błąd
    remainder = ''.join(encoded_data[-(len(poly) - 1):])
    errors = [i for i, bit in enumerate(remainder) if bit != '0']
    print(f"Correction errors at positions: {errors}")  # Debug print

    # Popraw błędy tylko na pozycjach ze zmiennej errors
    corrected_data = list(received_data)
    for error in crc_validate(received_data, polynomial):
        if corrected_data[error] == "1":
            corrected_data[error] = "0"
        else:
            corrected_data[error] = "1"

    return ''.join(corrected_data)
