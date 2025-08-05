import random
import string

def generate_random_chars(length=2):
    """Генерирует рандомные буквы (a-z)"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))