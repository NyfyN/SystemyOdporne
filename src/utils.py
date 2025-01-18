# Function to convert a word to its binary representation
def word_to_binary(word):
    return ''.join(format(ord(i), '08b') for i in word)

# Function to convert binary data back to a word
def binary_to_word(binary):
    n = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(i, 2)) for i in n)

# Function to highlight errors in the message
def highlight_errors(message, errors):
    """
    Highlights erroneous bits in the message. Erroneous bits are highlighted in red.
    """
    highlighted = ""
    for i, bit in enumerate(message):
        if i in errors:
            highlighted += f'<span style="color: red; font-weight: bold;">{bit}</span>'
        else:
            highlighted += bit
    return highlighted

# Function to highlight corrected bits in the message
def highlight_corrected(message, corrected):
    """
    Highlights corrected bits in the message. Corrected bits are highlighted in green.
    """
    highlighted = ""
    for i, bit in enumerate(message):
        if i in corrected:
            highlighted += f'<span style="color: #03fc17; font-weight: bold;">{bit}</span>'
        else:
            highlighted += bit
    return highlighted