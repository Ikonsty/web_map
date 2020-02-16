import ipaddress


def check_if_giving_information_is_valid(raw_address):
    """
    str -> str

    Function return raw_address if it is valid,
    write "Error" if raw_address is invalid and return None,
    or write "Missing prefix" if prefix is missed and return None

    >>> check_if_giving_information_is_valid("91.124.230.205/30")
    '91.124.230.205/30'
    """
    temp_address = raw_address
    n = 0
    for i in range(3):
        num_point = temp_address.find(".")
        if num_point == -1:
            break
        this_bit = temp_address[:num_point]

        if this_bit.isdigit() is False or int(this_bit) > 255 or int(this_bit) < 0:
            print("Error")
            return None
        temp_address = temp_address[num_point + 1:]
        n += 1
    if n != 3:
        print("Error")
        return None

    num_point = temp_address.find("/")
    if num_point == -1:
        print("Missing prefix")
        return None
    this_bit = temp_address[:num_point]

    if this_bit.isdigit() is False or int(this_bit) > 255 or int(this_bit) < 0:
        print("Error")
        return None

    this_bit = temp_address[num_point + 1:]

    if this_bit.isdigit() is False or int(this_bit) > 32 or int(this_bit) < 0:
        print("Error")
        return None

    return raw_address
# print(check_if_giving_information_is_valid("91.124.20.205/30"))


def convert_address_into_bin(address):
    """
    str -> str
    Make bin version of address
    >>> convert_address_into_bin("91.124.230.205")
    '01011011.01111100.11100110.11001101'
    """
    new_address = ''

    for i in range(3):
        num_point = address.find(".")
        this_bit = address[:num_point]
        this_bit = bin(int(this_bit))[2:]

        this_bit = this_bit.rjust(8, "0")
        new_address += this_bit + "."

        address = address[num_point + 1:]
    this_bit = address
    this_bit = bin(int(this_bit))[2:]

    this_bit = this_bit.rjust(8, "0")
    new_address += this_bit
    return new_address
# print(convert_address_into_bin("91.124.230.205"))


def convert_address_into_dec(address):
    """
    str -> str
    Make bin version of address
    >>> convert_address_into_dec('01011011.01111100.11100110.11001101')
    '91.124.230.205'
    """
    new_address = ''

    for i in range(3):
        num_point = address.find(".")
        this_bit = address[:num_point]
        this_bit = int(this_bit, 2)

        new_address += str(this_bit) + "."

        address = address[num_point + 1:]
    this_bit = address
    this_bit = int(this_bit, 2)

    new_address += str(this_bit)
    return new_address
# print(convert_address_into_dec('01011011.01111100.11100110.11001101'))


def get_ip_from_raw_address(raw_address):
    """
    str -> str
    Function return IP-address from raw_address
    >>> get_ip_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """
    address = check_if_giving_information_is_valid(raw_address)
    num_point = address.find("/")
    address = address[:num_point]
    return address
# print(get_ip_from_raw_address("91.124.230.205/30"))


def get_binary_mask_from_raw_address(raw_address):
    """
    str -> str
    Get mask from raw_address and convert into bin
    >>> get_binary_mask_from_raw_address('91.124.230.205/30')
    '11111111.11111111.11111111.11111100'
    """
    mask_bin = ''
    address = check_if_giving_information_is_valid(raw_address)
    num_point = address.find("/")
    mask_dec = int(address[num_point + 1:])
    mask_bin = mask_bin.ljust(mask_dec, "1")
    mask_bin = mask_bin.ljust(32, "0")

    n = 0
    mask_bin_point = ''
    for i in range(32):
        if i % 8 == 0 and i != 0:
            mask_bin_point += '.'
        mask_bin_point += mask_bin[i]
    return mask_bin_point
# print(get_binary_mask_from_raw_address("91.124.230.205/30"))


def get_network_address_from_raw_address(raw_address):
    """
    str -> str
    Return network address from IP and mask
    >>> get_network_address_from_raw_address("91.124.230.205/30")
    '91.124.230.204'
    """
    network_address = ''
    address = convert_address_into_bin(get_ip_from_raw_address(check_if_giving_information_is_valid(raw_address)))
    mask = get_binary_mask_from_raw_address(check_if_giving_information_is_valid(raw_address))

    for i in range(35):
        add_char = address[i]
        mask_char = mask[i]
        if add_char.isdigit() is False or mask_char.isdigit() is False:
            network_address += '.'
            continue
        network_address += str(int(add_char) & int(mask_char))
    network_address = convert_address_into_dec(network_address)
    return network_address
# print(get_network_address_from_raw_address("91.124.230.205/30"))


def get_broadcast_address_from_raw_address(raw_address):
    """
    str -> str
    Return Broadcast address from raw address
    >>> get_broadcast_address_from_raw_address("91.124.230.205/30")
    '91.124.230.207'
    """
    Broadcast_Address = ''
    address = convert_address_into_bin(get_ip_from_raw_address(check_if_giving_information_is_valid(raw_address)))
    mask = get_binary_mask_from_raw_address(check_if_giving_information_is_valid(raw_address))
    for i in range(35):
        add_char = address[i]
        mask_char = mask[i]
        if add_char.isdigit() is False or mask_char.isdigit() is False:
            Broadcast_Address += '.'
            continue
        Broadcast_Address += str(int(add_char) | (1 - int(mask_char)))
    Broadcast_Address = convert_address_into_dec(Broadcast_Address)
    return Broadcast_Address
# print(get_broadcast_address_from_raw_address("91.124.230.205/30"))


def next_address(address, change):
    """
    str -> str
    Return new address increased by change
    >>> next_address("91.124.230.254", 10)
    '91.124.239.255'
    """
    num_point = address.find(".")
    first_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    second_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    third_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    fourth_bit = int(address)

    for i in range(change):
        if fourth_bit + 1 <= 255:
            fourth_bit += 1
        elif third_bit + 1 <= 255:
            third_bit += 1
        elif second_bit + 1 <= 255:
            second_bit += 1
        elif first_bit + 1 <= 255:
            first_bit += 1
        else:
            return None
    new_address = str(first_bit) + "." + str(second_bit) + "." + str(third_bit) + "." + str(fourth_bit)
    return new_address
# print(next_address("91.124.230.205", 10))


def previous_address(address, change):
    """
    str -> str
    Return new address decreased by change
    >>> previous_address("91.124.230.254", 10)
    '91.124.230.244'
    """
    num_point = address.find(".")
    first_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    second_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    third_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    fourth_bit = int(address)

    for i in range(change):
        if fourth_bit - 1 >= 0:
            fourth_bit -= 1
        elif third_bit - 1 >= 0:
            third_bit -= 1
        elif second_bit - 1 >= 0:
            second_bit -= 1
        elif first_bit - 1 >= 0:
            first_bit -= 1
        else:
            return None
    new_address = str(first_bit) + "." + str(second_bit) + "." + str(third_bit) + "." + str(fourth_bit)
    return new_address
# print(previous_address("91.124.230.205", 10))


def get_first_usable_ip_address_from_raw_address(raw_address):
    """
    str -> str
    Return first usable ip address from raw_address
    >>> get_first_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """
    address = get_network_address_from_raw_address(raw_address)
    unable_ip = next_address(address, 1)
    return unable_ip
# print(get_first_usable_ip_address_from_raw_address("91.124.230.205/30"))


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    """
    str -> str
    Return get last usable ip address from raw address
    >>> get_penultimate_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.206'
    """
    address = get_broadcast_address_from_raw_address(raw_address)
    penultimate_ip = previous_address(address, 1)
    return penultimate_ip
# print(get_penultimate_usable_ip_address_from_raw_address("91.124.230.205/30"))


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """
    str -> num
    Return number of anable address
    >>> get_number_of_usable_hosts_from_raw_address("91.124.230.205/30")
    2
    """
    n = -1
    broadcast_address = get_broadcast_address_from_raw_address(raw_address)
    network_address = get_network_address_from_raw_address(raw_address)

    for i in range(3):
        num_point = broadcast_address.find(".")
        broadcast_address = broadcast_address[num_point + 1:]
        network_address = network_address[num_point + 1:]

    num_point = broadcast_address.find(".")
    fourth_bit_b = int(broadcast_address)
    fourth_bit_n = int(network_address)

    while n < 0:
        if fourth_bit_b - fourth_bit_n >= 0:
            n = fourth_bit_b - fourth_bit_n
        else:
            fourth_bit_b += 255
    return n - 1
# print(get_number_of_usable_hosts_from_raw_address("91.124.230.205/30"))


def get_ip_class_from_raw_address(raw_address):
    """
    str -> str
    Return version of raw_address
    >>> get_ip_class_from_raw_address("91.124.230.205/30")
    'A'
    """
    address = get_ip_from_raw_address(check_if_giving_information_is_valid(raw_address))
    num_point = address.find(".")
    first_bit = int(address[:num_point])

    if first_bit >= 0 and first_bit <= 127:
        class_address = "A"
    elif first_bit >= 128 and first_bit <= 191:
        class_address = "B"
    elif first_bit >= 192 and first_bit <= 223:
        class_address = "C"
    elif first_bit >= 224 and first_bit <= 239:
        class_address = "D(multicast)"
    elif first_bit >= 240 and first_bit <= 255:
        class_address = "E(reserved)"
    return class_address
# print(get_ip_class_from_raw_address("91.124.230.205/30"))


def check_private_ip_address_from_raw_address(raw_address):
    """
    str -> bool
    Return True if address is private, otherwise return False
    >>> check_private_ip_address_from_raw_address("91.124.230.205/30")
    False
    >>> check_private_ip_address_from_raw_address("192.168.93.15/30")
    True
    """
    address = get_ip_from_raw_address(check_if_giving_information_is_valid(raw_address))
    num_point = address.find(".")
    first_bit = int(address[:num_point])
    address = address[num_point + 1:]

    num_point = address.find(".")
    second_bit = int(address[:num_point])
    address = address[num_point + 1:]

    if first_bit == 10:
        return True
    elif first_bit == 172 and second_bit >= 16 and second_bit <= 31:
        return True
    elif first_bit == 192 and second_bit == 168:
        return True
    elif first_bit == 127:
        return True
    else:
        return False
# print(check_private_ip_address_from_raw_address("91.124.230.205/30"))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
