# Deobfuscated from: input/obf-main.py
# Original file: test_obf_5kb.py - obfuscator test
# Obfuscator: Zyphron v2.1 by DzyKhdra / KhangHo (Python 3.12)
# Deobfuscated by Antigravity

import math
import string
from collections import Counter, defaultdict

# --- 1. PRNG Generator (Zyphron alias: Trunks) ---
def prng(seed=1337):
    """Linear Congruential Generator (LCG) stream."""
    state = (seed ^ 1597463007) & 0x7FFFFFFF
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state

Trunks = prng


# --- 2. Quicksort (Zyphron alias: Rayquaza) ---
def quicksort(arr):
    """Recursive quicksort implementation."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

Rayquaza = quicksort


# --- 3. Memoization Decorator (Zyphron alias: Hokage728) ---
def memoize(fn):
    """Cache function results based on arguments."""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper

Hokage728 = memoize


# --- 4. Fibonacci (Zyphron alias: Nami474) ---
@memoize
def fib(n):
    """Memoized Fibonacci sequence calculation."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

Nami474 = fib


# --- 5. Caesar Cipher (Zyphron alias: Pikachu329) ---
def caesar(text, shift):
    """Shift alphabetical characters by `shift` positions."""
    res = []
    for c in text:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(c)
    return ''.join(res)

Pikachu329 = caesar


# --- 6. OOP Geometry Shapes (Zyphron aliases: Shanks283, DkhNgauVai, Nami, Drowned) ---
class Shape:
    """Base Shape class."""
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

    def perimeter(self):
        return 0

    def describe(self):
        return f'{self.name}: area={self.area():.2f}, perim={self.perimeter():.2f}'

Shanks283 = Shape


class Circle(Shape):
    def __init__(self, r):
        super().__init__('circle')
        self.r = r

    def area(self):
        return math.pi * self.r * self.r

    def perimeter(self):
        return 2 * math.pi * self.r

DkhNgauVai = Circle


class Rectangle(Shape):
    def __init__(self, w, h):
        super().__init__('rect')
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

Nami = Rectangle


class Triangle(Shape):
    def __init__(self, a, b, c):
        super().__init__('triangle')
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        s = self.perimeter() / 2
        try:
            return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        except ValueError:
            return 0.0

Drowned = Triangle


shapes = [
    Circle(3),
    Rectangle(4, 5),
    Triangle(3, 4, 5),
    Circle(1.5),
    Rectangle(2, 8)
]
Phantom321 = shapes


# --- 7. Shape Report (Zyphron alias: KhangHoDepTraiVaiCaLon386) ---
def shape_report(shape_list=None):
    """Aggregate statistics for a list of shape objects."""
    if shape_list is None:
        shape_list = shapes
    shape_data = [(s.name, round(s.area(), 2), round(s.perimeter(), 2)) for s in shape_list]
    total_area = round(sum(s.area() for s in shape_list), 2)
    biggest = max(shape_data, key=lambda x: x[1])
    return {
        'shapes': shape_data,
        'total_area': total_area,
        'biggest': biggest
    }

KhangHoDepTraiVaiCaLon386 = shape_report


# --- 8. Finite State Machine (Zyphron aliases: Chakra497, Zekrom763) ---
class StateMachine:
    STATES = {
        'idle': {'start': 'run'},
        'run': {'pause': 'paused', 'stop': 'idle'},
        'paused': {'resume': 'run', 'stop': 'idle'}
    }

    def __init__(self, initial='idle'):
        self.state = initial

    def send(self, event):
        trans = self.STATES.get(self.state, {})
        if event in trans:
            nxt = trans[event]
            res = ('ok', self.state, event)
            self.state = nxt
            return res
        return ('reject', self.state, event)

Chakra497 = StateMachine


def run_fsm(events):
    """Execute a sequence of events through the StateMachine."""
    fsm = StateMachine()
    log = []
    for ev in events:
        res = fsm.send(ev)
        log.append(res)
    return fsm.state, log

Zekrom763 = run_fsm


# --- 9. Text Word Statistics (Zyphron alias: Wither67) ---
def word_stats(text):
    """Analyze word frequency and lengths in a string."""
    words = [w.strip(string.punctuation).lower() for w in text.split()]
    words = [w for w in words if w]
    counts = Counter(words)
    return {
        'count': len(words),
        'unique': len(counts),
        'top': counts.most_common(3),
        'longest': max(len(w) for w in words) if words else 0
    }

Wither67 = word_stats


# --- 10. Collatz Sequence Length (Zyphron alias: Villager) ---
def collatz(n):
    """Compute number of steps to reach 1 in Collatz conjecture."""
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

Villager = collatz


# --- 11. Prime Number Sieve (Zyphron alias: ZyphronObfuscatorDinhQua) ---
def primes(n):
    """Sieve of Eratosthenes returning all primes below n."""
    sieve = [True] * n
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            for j in range(i * i, n, i):
                sieve[j] = False
    return [i for i in range(2, n) if sieve[i]]

ZyphronObfuscatorDinhQua = primes


# --- 12. XOR Cipher (Zyphron alias: Buu) ---
def xor_cipher(data, key):
    """Repeated-key XOR byte transformation."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

Buu = xor_cipher


# --- 13. Main Execution Entry Point (Zyphron alias: Ender922) ---
def main():
    r = prng()
    stream = [next(r) % 100 for _ in range(12)]
    print('stream:', stream)
    print('sorted:', quicksort(stream))
    print('fib(20):', fib(20))
    print('caesar:', caesar('Obfuscator Test 2026!', 7))
    for s in shapes:
        print(s.describe())
    print('report:', shape_report(shapes))
    state, log = run_fsm(['start', 'pause', 'resume', 'stop'])
    print('events:', state, log)
    print('stats:', word_stats('The quick brown fox jumps over the lazy dog; the fox!'))
    print('collatz(27):', collatz(27))
    print('primes<50:', primes(50))
    print('xor roundtrip:', xor_cipher(xor_cipher(b'payload', b'key12345'), b'key12345') == b'payload')
    print('OK')

Ender922 = main

if __name__ == '__main__':
    main()
