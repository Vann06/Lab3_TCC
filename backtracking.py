from shunting_yard import expand_clases, add_concat, to_postfix
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from pathlib import Path
import os, re, sys

class TreeNode:
    def __init__(self, v):
        self.value = v
        self.left = None
        self.right = None
        self.x = 0 
        self.y = 0

def build_tree(postfix: str):
    """
    Construye un árbol de expresión a partir de una notación postfija.
    """
    # tipos operandos   
    bin_ops = {'.', '°', '|'}
    una_ops = {'*', '+', '?'}
    stack   = []

    tokens = postfix.split() if ' ' in postfix else list(postfix)

    for tok in tokens:
        if tok.startswith('{') and tok.endswith('}'):
            child = stack.pop(); n = TreeNode(tok); n.left = child; stack.append(n)
        elif tok.startswith('[') and tok.endswith(']') or tok.startswith('\\') or tok == 'ε' or tok.isalnum():
            stack.append(TreeNode(tok))
        elif tok in bin_ops:
            r, l = stack.pop(), stack.pop(); n = TreeNode(tok); n.left, n.right = l, r; stack.append(n)
        elif tok in una_ops:
            child = stack.pop(); n = TreeNode(tok); n.left = child; stack.append(n)
    return stack[0] if len(stack) == 1 else None

def _w(n): return 0 if not n else 1 if not n.left and not n.right else _w(n.left)+_w(n.right)

def _set_xy(n, xl, d, h=1.4, v=1.8):
    if not n: return
    wl = _w(n.left); wr = _w(n.right); sw = max(1, wl+wr)
    n.x = (xl+sw/2)*h; n.y = -d*v
    _set_xy(n.left, xl, d+1); _set_xy(n.right, xl+wl, d+1)

def draw_tree(root, original, postfix, png):
    if not root: return
    _set_xy(root, 0, 0)
    xs, ys = [], []
    def walk(n): 
        if n: xs.append(n.x); ys.append(n.y); walk(n.left); walk(n.right)
    walk(root)
    fig, ax = plt.subplots(figsize=(max(6,max(xs)-min(xs)+2), max(4,abs(min(ys))+2)))
    ax.set_xlim(min(xs)-1, max(xs)+1); ax.set_ylim(min(ys)-1, 1); ax.axis('off')
    ax.set_title(f"Árbol — {original}\nPostfix: {postfix}")

    def edges(n):
        if n.left: ax.plot([n.x, n.left.x],[n.y, n.left.y],'k-', zorder=0); edges(n.left)
        if n.right: ax.plot([n.x, n.right.x],[n.y, n.right.y],'k-', zorder=0); edges(n.right)

    def nodes(n):
        if n.value in {'.','°','|','*','+','?'} or n.value.startswith('{'):
            circ = plt.Circle((n.x,n.y),0.25,fc='mediumpurple',ec='purple',zorder=3)
            ax.add_patch(circ)
            ax.text(n.x,n.y,'.' if n.value=='°' else n.value,
                    ha='center',va='center',color='white',zorder=4)
        else:
            rect = Rectangle((n.x-0.25,n.y-0.25),0.5,0.5,fc='lightblue',ec='blue',zorder=3)
            ax.add_patch(rect)
            ax.text(n.x,n.y,n.value,ha='center',va='center',color='darkblue',zorder=4)
        if n.left: nodes(n.left); 
        if n.right: nodes(n.right)

    edges(root); nodes(root)
    ax.legend(handles=[mpatches.Patch(color='mediumpurple',label='Operador'),
                       mpatches.Patch(color='lightblue',label='Operando')])
    plt.tight_layout(); plt.savefig(png,dpi=300,bbox_inches='tight'); plt.close()

def process_expression(expr, out_png):
    expr = expr.replace(' ', '')                              # quitar espacios
    expr = add_concat(expand_clases(expr))                    # usar shunting_yard
    postfix = to_postfix(expr)
    tree = build_tree(postfix)
    if tree:
        draw_tree(tree, expr, postfix, out_png)
        return True
    return False

def process_file(path='expresiones_arbol.txt'):
    out_dir = Path('arboles_sintacticos'); out_dir.mkdir(exist_ok=True)
    for i, raw in enumerate(Path(path).read_text(encoding='utf8').splitlines(),1):
        raw = raw.strip()
        if not raw: continue
        file_name = re.sub(r'[^a-zA-Z0-9]', '_', raw)[:40]
        ok = process_expression(raw, out_dir / f'{i}_{file_name}.png')
        if not ok: print(f'línea {i} falló')

if __name__ == '__main__':
    if len(sys.argv)==2: process_file(sys.argv[1])
    else: process_file()
