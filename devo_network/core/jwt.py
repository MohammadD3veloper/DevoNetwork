from rest_framework_simplejwt.tokens import RefreshToken


def generate_token_for_user(user):
    """ Generate jwt tokens for each user """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def set_token_to_blacklist(token):
    """ Set given token into blacklist """
    token = RefreshToken(token)
    token.blacklist()
    return True
