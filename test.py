from datetime import datetime

if __name__ == '__main__':
    def hex_to_binary(hex_string):
        # Split the string by '0x' and filter out empty strings
        hex_bytes = hex_string.split('0x')[1:]  # The first split part is empty

        # Convert each hex byte to its binary representation and pad to 8 bits
        binary_string = ''.join(format(int(byte, 16), '08b') for byte in hex_bytes)

        return binary_string
    def add_prefix(binary_string):
        # Ensure the binary string length is even
        if len(binary_string) % 2 != 0:
            raise ValueError("The length of the binary string should be even.")

        # Add "0x" to the front of each two characters
        result = ''.join(f"0x{binary_string[i:i + 2]}" for i in range(0, len(binary_string), 2))

        return result


    # Example binary string
    binary_string = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000901000000000000'

    # Transform the binary string
    transformed_string = add_prefix(binary_string)

    print(transformed_string)

    binary = hex_to_binary(transformed_string)
    print(binary)


    def extract_fields_to_array(binary_string, field_lengths):
        result = {}
        position = 0

        for field, length in field_lengths.items():
            array = []
            for _ in range(length):
                # Each field is assumed to be 16 bits (2 bytes)
                field_value = binary_string[position:position + 16]
                array.append(int(field_value, 2))
                position += 16
            result[f'{field}'] = array
        return result


    # Given binary string
    binary_string = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100100000001000000000000000000000000000000000000000000000000"

    print(len(binary_string))
    # Define the lengths of each field in bytes
    field_lengths = {
        'usVelocity': 3,
        'usDisplacement': 3,
        'usAcceleration': 3,
        'usVelocityPeak': 3,
        'usAccelerationPeak': 3,
        'usVelocityKurtosis': 3,
        'usAccelerationKurtosis': 3,
        'usVelocitySpectrum': 3 * 8,
        'usAccelerationSpectrum': 3 * 8,
        'usRotateVelocitySpectrum_Z': 8,
        'usTemp': 1,
        'usRotateHz': 3
    }

    # Extract the fields from the binary string into a one-dimensional array
    array = extract_fields_to_array(binary_string, field_lengths)

    print(array)

