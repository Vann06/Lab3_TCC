# Algoritmo Shunting Yard para Expresiones Regulares


# Precedencia de operadores - números más altos = mayor precedencia  
PRECEDENCE = {
    '*': 3,  # Estrella de Kleene (cero o más)
    '+': 3,  # Más (uno o más) 
    '?': 3,  # Interrogación (cero o uno)
    '.': 2,  # Concatenación implícita
    '|': 1,  # Alternancia (OR)
}

# Asociatividad - determinamos cómo agrupar operadores de igual precedencia
LEFT_ASSOCIATIVE = {'.', '|'}
RIGHT_ASSOCIATIVE = {'*', '+', '?'}


def insert_concatenation(expression):
    """
    Inserta '.' de concatenación donde corresponde.
    Se eliminan todos los espacios antes de procesar.
    """
    # 1) quitar espacios
    expression = expression.replace(' ', '')
    
    result = ''
    for i, current in enumerate(expression):
        result += current

        if i + 1 < len(expression):
            next_char = expression[i + 1]

            if (
                (current.isalnum() or current in {'ε', '*', '+', '?', ')'})
                and
                (next_char.isalnum() or next_char == 'ε' or next_char == '(')
            ):
                result += '.'

    return result




def to_postfix(expression):
    """
    Convierte expresión infix a postfix usando algoritmo Shunting Yard
    Versión mejorada con mejor manejo de casos especiales
    """
    output = []
    operator_stack = []
    steps = []
    
    i = 0
    while i < len(expression):
        token = expression[i]
        
        # Manejar caracteres escapados
        if token == '\\' and i + 1 < len(expression):
            escaped_char = token + expression[i + 1]
            output.append(escaped_char)
            steps.append(f"Carácter escapado '{escaped_char}' → salida: {output}")
            i += 2  # saltar ambos caracteres
            continue
        
        # Operandos (letras, números, épsilon)
        if token.isalnum() or token == 'ε':
            output.append(token)
            steps.append(f"Operando '{token}' → salida: {output}")
            
        # Paréntesis de apertura
        elif token == '(':
            operator_stack.append(token)
            steps.append(f"'(' → pila: {operator_stack}")
            
        # Paréntesis de cierre
        elif token == ')':
            # Vaciar pila hasta encontrar '('
            while operator_stack and operator_stack[-1] != '(':
                operator = operator_stack.pop()
                output.append(operator)
                steps.append(f"Vaciar hasta '(' → '{operator}' a salida: {output}")
            
            # Quitar el '(' de la pila
            if operator_stack:
                operator_stack.pop()
                steps.append("Remover '(' de la pila")
                
        # Operadores
        elif token in PRECEDENCE:
            # Aplicar reglas de precedencia y asociatividad
            while (
                operator_stack and 
                operator_stack[-1] in PRECEDENCE and
                (
                    PRECEDENCE[operator_stack[-1]] > PRECEDENCE[token] or
                    (PRECEDENCE[operator_stack[-1]] == PRECEDENCE[token] and 
                     token in LEFT_ASSOCIATIVE)
                )
            ):
                operator = operator_stack.pop()
                output.append(operator)
                steps.append(f"Precedencia: '{operator}' → salida: {output}")
            
            operator_stack.append(token)
            steps.append(f"Operador '{token}' → pila: {operator_stack}")
        
        i += 1
    
    # Vaciar pila restante
    while operator_stack:
        operator = operator_stack.pop()
        output.append(operator)
        steps.append(f"Vaciar pila final → '{operator}' a salida: {output}")
    
    return ''.join(output), steps


def get_only_postfix(expression):
    """
    Convierte expresión infix a postfix y devuelve solo la notación postfija
    """
    with_concat = insert_concatenation(expression)
    postfix, _ = to_postfix(with_concat)
    return postfix


def process_file(filename):
    """
    Procesa archivo con expresiones regulares y las convierte a notación postfija
    Versión mejorada con mejor formato de salida
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_number = 0
            
            for line in file:
                original_expression = line.strip()
                
                # Saltear líneas vacías
                if not original_expression:
                    continue
                
                line_number += 1
                print(f"\n{'='*50}")
                print(f"EXPRESIÓN {line_number}: {original_expression}")
                print(f"{'='*50}")
                
                # Paso 1: Insertar concatenaciones explícitas
                with_concat = insert_concatenation(original_expression)
                print(f"Con concatenaciones: {with_concat}")
                
                # Paso 2: Convertir a postfijo
                postfix_result, steps = to_postfix(with_concat)
                
                # Mostrar proceso paso a paso
                print("\nProceso paso a paso:")
                for i, step in enumerate(steps, 1):
                    print(f"  {i:2d}. {step}")
                
                print(f"\n✓ RESULTADO FINAL: {postfix_result}")
                
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
    except UnicodeDecodeError:
        print(f"Error: Problema de codificación en el archivo '{filename}'")
    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    process_file("expresiones.txt")