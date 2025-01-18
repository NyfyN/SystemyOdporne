import random

class CRC:
    
    def __init__(self):
        # Initialize the CRC class with an empty codeword
        self.cdw = ''

    def xor(self, a, b):
        # Perform XOR operation between two binary strings
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
        return ''.join(result)

    def crc(self, message, key):
        # Calculate the CRC remainder for the given message and key
        pick = len(key)
        tmp = message[:pick]

        while pick < len(message):
            if tmp[0] == '1':
                tmp = self.xor(key, tmp) + message[pick]
            else:
                tmp = self.xor('0' * pick, tmp) + message[pick]
            pick += 1

        if tmp[0] == "1":
            tmp = self.xor(key, tmp)
        else:
            tmp = self.xor('0' * pick, tmp)

        checkword = tmp
        return checkword

    def encodedData(self, data, key):
        # Encode the data using the provided key and store the codeword
        l_key = len(key)
        append_data = data + '0' * (l_key - 1)
        remainder = self.crc(append_data, key)
        codeword = data + remainder
        self.cdw = codeword

    def introduceError(self, data):
        # Introduce random errors into the data
        error_data = list(data)
        amount_of_errors = random.randint(0, len(data) - 1)
        positions = [position for position in range(len(data))]
        error_positions = random.sample(positions, amount_of_errors)
        
        for position in error_positions:
            if error_data[position] not in ('0', '1'):
                raise ValueError(f"Unexpected character '{error_data[position]}' in binary data.")
            error_data[position] = '1' if error_data[position] == '0' else '0'
        
        return ''.join(error_data), error_positions