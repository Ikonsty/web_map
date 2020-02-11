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

        if this_bit.isdigit() == False or int(this_bit) > 256 or int(this_bit) < 0:
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

    if this_bit.isdigit() == False or int(this_bit) > 256 or int(this_bit) < 0:
        print("Error")
        return None

    this_bit = temp_address[num_point + 1:]

    if this_bit.isdigit() == False or int(this_bit) > 256 or int(this_bit) < 0:
        print("Error")
        return None

    return raw_address
print(check_if_giving_information_is_valid("91.124.20.205/30"))


# def get_ip_from_raw_address(raw_address):
#     """
#     str -> str
#     Function return IP-address from raw_address
#     >>> get_ip_from_raw_address("91.124.230.205/30")
#     91.124.230.205
#     """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
