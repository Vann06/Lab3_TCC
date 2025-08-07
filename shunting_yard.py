# Algoritmo Shunting Yard para Expresiones Regulares

import re, sys
from pathlib import Path

# precedencia y asociatividad
PRECEDENCE = {'|': 1, '°': 2, '*': 3, '+': 3, '?': 3}  
LEFT = {'|', '°'}

CONCAT_PREV = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ε)*+?}')
CONCAT_NEXT = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ε([')


def expand_clases(expr: str) -> str:
    """
    expandir clases de caracteres:
    [ab]  →  (a|b)
    """
    return re.sub(r'\[([^]]+)]',
                  lambda m: m.group(1) if len(m.group(1)) == 1 else '(' + '|'.join(m.group(1)) + ')',
                  expr)

def add_concat(expr: str) -> str:
    out = []
    for i, ch in enumerate(expr):
        out.append(ch)
        if i + 1 < len(expr):
            nx = expr[i + 1]
            if ch in CONCAT_PREV and nx in CONCAT_NEXT and nx not in '|*+?{':
                out.append('°')
    return ''.join(out)

# tokenización: clases, escapes, cuantificadores, operadores y literales
TOKEN = re.compile(r'''
    \[[^]]+]        |   # clase de caracteres
    \\ .            |   # carácter escapado
    \{[^}]+}        |   # cuantificador {n}, {n,}, {n,m}
    [()*+?|°]        |   # operadores y paréntesis
    [^()*+?|°\[\\{}\s]   # literales (excluye espacios)
''', re.X)

prec  = lambda op: 3 if op.startswith('{') else PRECEDENCE[op]
left  = lambda op: False if op.startswith('{') else op in LEFT



def to_postfix(expr: str) -> str:
    expr = expr.replace(' ', '')  # quitar espacios
    output, stack = [], []
    for tok in TOKEN.findall(expr):
        if tok not in PRECEDENCE and tok not in '()*+?|°' and not tok.startswith('{'):
            output.append(tok)
            continue
        if tok == '(':  # apilar paréntesis
            stack.append(tok)
            continue
        if tok == ')':  # vaciar hasta '('
            while stack and stack[-1] != '(': output.append(stack.pop())
            if stack: stack.pop()
            continue
        # operadores (incl. cuantificadores)
        while stack and stack[-1] != '(':  # comparar precedencia
            top = stack[-1]
            if prec(top) > prec(tok) or (prec(top) == prec(tok) and left(tok)):
                output.append(stack.pop())
            else:
                break
        stack.append(tok)
    while stack:
        output.append(stack.pop())
    return ' '.join(output)


def process_file(path: str):
    for n, raw in enumerate(Path(path).read_text(encoding='utf8').splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        expr = add_concat(expand_clases(raw))
        print(f'# {n} {raw}\n{to_postfix(expr)}\n')

if __name__ == '__main__':
    process_file(sys.argv[1])
