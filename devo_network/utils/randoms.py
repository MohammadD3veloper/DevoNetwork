import random
import string


def generate_group_address():
    """ Generate random ascii string """
    # TODO: Generate random ascii string
    ...


def generate_otp_code():
    """ Generate otp code for registration """
    otp_code = random.randrange(10000, 99999)
    return otp_code
