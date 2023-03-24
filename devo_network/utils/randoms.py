import random
import string


def generate_group_address():
    """ Generate random ascii string """
    # TODO: Generate random ascii string
    items = string.ascii_lowercase + string.ascii_uppercase + '-_+=@'
    address = ''.join(
        random.choice(items) for i in range(0, 24)
    )
    print(address)
    return address


def generate_otp_code():
    """ Generate otp code for registration """
    otp_code = random.randrange(10000, 99999)
    return otp_code
