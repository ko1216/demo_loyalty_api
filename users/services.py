import random
import string

from users.models import User


def generate_invite_code():
    characters = string.ascii_letters + string.digits

    while True:
        invite_code = ''.join(random.choices(characters, k=6))
        if not User.objects.filter(invite_code=invite_code).exists():
            return invite_code
