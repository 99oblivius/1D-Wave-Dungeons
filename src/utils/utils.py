import string

def clamp(x, a, b):
    assert (a <= b)
    return max(a, min(b, x))

def plural(value) -> str:
    return 's' if value != 1 else ''

def clear_screen():
    print(end="\033c", flush=True)

def obfuscated(s: str, ch: str='#') -> str:
    allowed_chars = string.whitespace + string.punctuation
    return ''.join(char if char in allowed_chars else ch for char in s)

def ellipse_justified(s: str, l: int=10):
    return (f'{s:.{l-1}}' + ('\u2026' if len(s) > l else '')).ljust(l)
