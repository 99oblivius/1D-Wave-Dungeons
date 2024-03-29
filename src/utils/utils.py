def clamp(x, a, b):
  assert (a <= b)
  return max(a, min(b, x))

def plural(value) -> str:
  return 's' if value != 1 else ''

def clear_screen():
  print(end="\033c", flush=True)