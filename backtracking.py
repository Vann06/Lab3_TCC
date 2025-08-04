from shunting_yard import get_only_postfix
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Rectangle
import numpy as np
import os

class TreeNode:
    """
    Clase para representar un nodo en el árbol de expresión.
    """
    def __init__(self, value):
        self.value = value # simbolo u operador
        self.left = None # hijo izquierdo
        self.right = None # hijo derecho
        self.x = 0
        self.y = 0

    def __repr__(self):
        return f"TreeNode({self.value})"
    

def build_tree(postfix):
    """
    Construye un árbol de expresión a partir de una notación postfija.
    """
    stack = []

    # tipos operandos
    binary_operators = {'.', '|',}      # 2 hijos DER
    unary_operators = {'*', '+', '?'}   # 1 hijo  IZQ

    print(f"Construyendo arbol desde postfix: '{postfix}'")


    for i, token in enumerate(postfix):
        if token.isalnum() or token == 'ε':  # Si es un operando
            node = TreeNode(token)
            stack.append(node)
        else:
            if token in binary_operators:
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    node = TreeNode(token)
                    node.left = left
                    node.right = right
                    stack.append(node)
                else:
                    print(f"Error: No hay suficientes operandos para el operador '{token}'")
                    return None
            elif token in unary_operators:
                if len(stack) >= 1:
                    child = stack.pop()
                    node = TreeNode(token)
                    node.left = child # solo al izq
                    stack.append(node)
                else:
                    print(f"Error: No hay suficientes operandos para el operador '{token}'")
                    return None

    return stack[0] if len(stack) == 1 else None


def calculate_positions(root, h_unit=1.4, v_unit=1.8):
    """
    Asigna coordenadas (x, y) a cada nodo:
    - 'h_unit' es la distancia horizontal básica entre columnas.
    - 'v_unit' es la distancia vertical entre niveles.
    """

    def _width(n):
        """Devuelve el número de columnas que ocupa el sub-árbol."""
        if n is None:
            return 0
        if n.left is None and n.right is None:
            return 1
        return _width(n.left) + _width(n.right)

    def _set_xy(n, x_left, depth=0):
        """
        Coloca el nodo en medio de su bloque [x_left, x_left+subWidth).
        Devuelve la anchura usada.
        """
        if n is None:
            return 0
        w_left  = _width(n.left)
        w_right = _width(n.right)
        # ancho total de ESTE sub-árbol
        sub_width = max(1, w_left + w_right)

        # centro geométrico
        center = x_left + sub_width / 2
        n.x = center * h_unit
        n.y = -depth * v_unit

        # hijos
        _set_xy(n.left,  x_left,                depth + 1)
        _set_xy(n.right, x_left + w_left,       depth + 1)
        return sub_width

    _set_xy(root, 0)          # arranca colocando la raíz

def draw_tree(root, original_expression, postfix_expression, filename=None):
    if root is None:
        print("No se pudo construir el árbol.")
        return

    # a) posicionar
    calculate_positions(root)

    # b) obtener límites reales
    xs, ys = [], []
    def walk(n):
        if n:
            yield from walk(n.left)
            xs.append(n.x); ys.append(n.y)
            yield from walk(n.right)
    list(walk(root))
    min_x, max_x = min(xs), max(xs)
    min_y = min(ys)

    # margen estético
    margin_x = 1.0
    margin_y = 1.0

    # c) figura proporcional al ancho y profundidad
    width  = max(6, (max_x - min_x) + 2 * margin_x)
    height = max(4, (abs(min_y) + margin_y + 1))
    fig, ax = plt.subplots(figsize=(width, height))

    title = (f"Árbol Sintáctico\n"
             f"Expresión: {original_expression}\n"
             f"Postfix: {postfix_expression}")
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(min_x - margin_x, max_x + margin_x)
    ax.set_ylim(min_y - margin_y, 1 + margin_y)  # raíz siempre visible arriba
    ax.axis('off')

    # --- dibujo auxiliar ---
    def draw_edges(n):
        if n.left:
            ax.plot([n.x, n.left.x], [n.y, n.left.y], 'k-', lw=1.8, zorder=1)
            draw_edges(n.left)
        if n.right:
            ax.plot([n.x, n.right.x], [n.y, n.right.y], 'k-', lw=1.8, zorder=1)
            draw_edges(n.right)

    def draw_nodes(n):
        if n.value in {'.', '|', '*', '+', '?'}:
            c = plt.Circle((n.x, n.y), 0.25, fc='mediumpurple',
                           ec='purple', lw=2)
            ax.add_patch(c)
            ax.text(n.x, n.y, n.value, ha='center', va='center',
                    color='white', fontweight='bold', fontsize=14)
        else:
            r = Rectangle((n.x - 0.25, n.y - 0.25), 0.5, 0.5,
                          fc='lightblue', ec='blue', lw=2)
            ax.add_patch(r)
            ax.text(n.x, n.y, n.value, ha='center', va='center',
                    color='darkblue', fontweight='bold', fontsize=12)
        if n.left:  draw_nodes(n.left)
        if n.right: draw_nodes(n.right)

    # d) dibujar
    draw_edges(root)
    draw_nodes(root)

    # e) leyenda
    operator_patch = mpatches.Patch(color='mediumpurple', label='Operadores')
    operand_patch  = mpatches.Patch(color='lightblue',   label='Operandos')
    ax.legend(handles=[operator_patch, operand_patch], loc='upper right')

    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Árbol guardado como: {filename}")
        plt.close()
    else:
        plt.show()

def process_expression(expression, save_file=None):
    print(f"\nPROCESANDO: {expression}")
    print("-" * 50)
    
    postfix = get_only_postfix(expression)
    print(f"Postfix: {postfix}")
    
    tree_root = build_tree(postfix)
    
    if tree_root:
        print("Arbol construido exitosamente")
        draw_tree(tree_root, expression, postfix, save_file)
        return tree_root
    else:
        print("Error al construir el arbol")
        return None

# Modifica solo la función process_file para hacer debug

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            expressions = [line.strip() for line in file if line.strip()]
        
        # DEBUG: Mostrar qué expresiones se leyeron
        print("GENERADOR DE ARBOLES SINTACTICOS")
        print("=" * 50)
        print(f"Archivo leido: {filename}")
        print(f"Expresiones encontradas: {len(expressions)}")
        for i, expr in enumerate(expressions, 1):
            print(f"  {i}. '{expr}'")
        print("-" * 30)
        
        # Crear carpeta para guardar los árboles
        output_folder = "arboles_sintacticos"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Carpeta creada: {output_folder}")
        
        for i, expr in enumerate(expressions, 1):
            print(f"\nPROCESANDO Expresion {i} de {len(expressions)}: '{expr}'")
            
            try:
                # Crear nombre de archivo seguro
                safe_expr = expr.replace("(", "").replace(")", "").replace("|", "o").replace("*", "star").replace("+", "plus").replace("?", "opt").replace(" ", "_")
                output_file = os.path.join(output_folder, f"expresion_{i}_{safe_expr}.png")
                
                print(f"Guardando como: {output_file}")
                
                tree = process_expression(expr, output_file)

                if tree:
                    print(f"EXITO: Expresion {i} completada")
                else:
                    print(f"ERROR: Fallo en expresion {i}")

            except Exception as e:
                print(f"EXCEPCION en expresion {i}: {e}")
                continue
            
        print(f"\nPROCESO COMPLETADO")
        print(f"TODOS LOS ARBOLES GUARDADOS EN: {output_folder}")
        print("\nArchivos generados:")
        
        if os.path.exists(output_folder):
            files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
            if files:
                for file in sorted(files):
                    print(f"  {file}")
            else:
                print("  No se generaron archivos PNG")
        
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo '{filename}'")
    except Exception as error:
        print(f"Error general: {error}")

if __name__ == "__main__":
    process_file("expresiones_arbol.txt")