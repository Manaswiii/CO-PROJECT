def string_to_12bit_twos_complement_binary(input_string):
    try:
        input_integer = int(input_string)
    except ValueError:
        return "Invalid input: not a valid integer"

    if input_integer < -2**11 or input_integer > 2**11 - 1:
        return "Input integer out of range for 12-bit two's complement"

    if input_integer < 0:
        # For negative numbers, we'll use 2's complement representation
        input_binary = bin((1 << 12) + input_integer)[2:]
    else:
        input_binary = bin(input_integer)[2:]

    input_binary = input_binary.zfill(12)

    return input_binary

# Test the function
input_string = input("Enter an integer: ")
binary_representation = string_to_12bit_twos_complement_binary(input_string)
print("12-bit two's complement binary representation:", binary_representation)

