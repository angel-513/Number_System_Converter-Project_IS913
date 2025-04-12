import ply.yacc as yacc
import random
from anly_lex import tokens, lexer

def get_original_format(num_str):
    if isinstance(num_str, str):
        if num_str.lower().startswith('0b'):
            return 'binary'
        elif num_str.lower().startswith('0o'):
            return 'octal'
        elif num_str.lower().startswith('0x'):
            return 'hexadecimal'
        else:
            return 'decimal'
    
    return 'roman'

def p_convert(p):
    '''convert : number TO format'''
    num_str, num = p[1]
    target_format = p[3]

    if target_format == 'random':
        original_format = get_original_format(num_str)
        formats = ['binary', 'octal', 'hexadecimal', 'decimal', 'roman', 'ternary']
        formats.remove(original_format)
        target_format = random.choice(formats)
    
    try:
        if target_format == 'binary':
            result = bin(num)[2:]
        elif target_format == 'octal':
            result = oct(num)[2:]
        elif target_format == 'hexadecimal':
            result = hex(num)[2:]
        elif target_format == 'decimal':
            result = str(num)
        elif target_format == 'roman':
            result = int_to_roman(num)
        elif target_format == 'ternary':
            result = int_to_base(num, 3)
        else:
            result = "Formato no válido"
    except ValueError as e:
        result = f"Error: {e}"

    p[0] = f"Resultado: {result} en {target_format}"

def p_number(p):
    '''number : BINARY
              | OCTAL
              | HEXADECIMAL
              | DECIMAL
              | ROMAN
              | TERNARY'''
    base = 10
    prefix = p[1][:2].lower() if isinstance(p[1], str) else ''

    if prefix == '0b':
        base = 2
    elif prefix == '0o':
        base = 8
    elif prefix == '0x':
        base = 16
    elif prefix == '0t':
        base = 3
    
    if isinstance(p[1], int):
        p[0] = ('roman', p[1])
    else:
        p[0] = (p[1], int(p[1], base))

def p_format(p):
    '''format : FMT_BINARY
              | FMT_OCTAL
              | FMT_DECIMAL
              | FMT_HEXADECIMAL
              | FMT_ROMAN
              | FMT_TERNARY
              | RANDOM'''
    p[0] = p[1].lower()

def int_to_roman(num):
    if not (0 < num < 4000):
        raise ValueError("El número debe estar entre 1 y 3999")
    
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4, 1
    ]

    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV", "I"
    ]
    roman = ""
    
    i=0
    while num > 0:
        for _ in range(num // val[i]):
            roman += syms[i]
            num -= val[i]
        i += 1

    return roman

def int_to_base(num, base):
    if num == 0:
        return '0'
    
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base

    return ''.join(reversed(digits))

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}'")
    else:
        print(f"Error de sintaxis: entrada incompleta o vacia.")

parser = yacc.yacc()

def parse_input(data):
    return parser.parse(data, lexer=lexer)