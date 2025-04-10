import ply.lex as lex
import re

reserved = {
    'to': 'TO',
    'random': 'RANDOM',
    'binary': 'FMT_BINARY',
    'octal': 'FMT_OCTAL',
    'decimal': 'FMT_DECIMAL',
    'hexadecimal': 'FMT_HEXADECIMAL',
    'roman': 'FMT_ROMAN'
}

tokens = [
    'DECIMAL', 'BINARY', 'OCTAL', 'HEXADECIMAL', 'ROMAN'
] + list(reserved.values())

t_ignore = ' \t'

def t_BINARY(t):
    r'0[bB][01]+'
    try:
        int(t.value, 2)
        return t
    except ValueError:
        print(f"Error: numero binario invalido '{t.value}'")
        t.lexer.skip(len(t.value))

def t_OCTAL(t):
    r'0[oO][0-7]+'
    try:
        int(t.value, 8)
        return t
    except ValueError:
        print(f"Error: numero octal invalido '{t.value}'")
        t.lexer.skip(len(t.value))

def t_HEXADECIMAL(t):
    r'0[xX][0-9a-fA-F]+'
    try:
        int(t.value, 16)
        return t
    except ValueError:
        print(f"Error: numero hexadecimal invalido '{t.value}'")
        t.lexer.skip(len(t.value))

def t_DECIMAL(t):
    r'\d+'
    try:
        int(t.value)
        return t
    except ValueError:
        print(f"Error: numero decimal invalido '{t.value}'")
        t.lexer.skip(len(t.value))

def t_ROMAN(t):
    r'[IVXLCDM]+'

    if t.value == '':
        return None

    if is_valid_roman(t.value):
        t.value = roman_to_int(t.value)
        return t
    else:
        print(f"Error: numero romano invalido '{t.value}")
        t.lexer.skip(len(t.value))

def is_valid_roman(s):
    pattern = re.compile(r'^M{0,3}(CM|CD|D?C{0,3})'
                         r'(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
    return bool(pattern.fullmatch(s.upper()))

def roman_to_int(s):
    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    total = 0
    prev = 0

    for char in reversed(s.upper()):
        if roman_map[char] < prev:
            total -= roman_map[char]
        else:
            total += roman_map[char]
            prev = roman_map[char]
    
    return total

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()