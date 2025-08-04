# Generador de Árboles Sintácticos para Expresiones Regulares

Este proyecto implementa un generador de árboles sintácticos para expresiones regulares, utilizando el algoritmo Shunting Yard para convertir expresiones infijas a notación postfija y posteriormente construir representaciones visuales de los árboles sintácticos.

## 📋 Descripción

El proyecto consta de tres componentes principales:

1. **Algoritmo Shunting Yard** (`shunting_yard.py`): Convierte expresiones regulares en notación infija a notación postfija
2. **Constructor de Árboles** (`backtracking.py`): Construye y visualiza árboles sintácticos a partir de expresiones postfijas
3. **Archivo de Expresiones** (`expresiones_arbol.txt`): Contiene las expresiones regulares a procesar

## 🚀 Características

- ✅ Conversión automática de expresiones infijas a postfijas
- ✅ Construcción de árboles sintácticos
- ✅ Visualización gráfica con matplotlib
- ✅ Soporte para operadores: `*` (Kleene), `+` (uno o más), `?` (opcional), `|` (alternancia), `.` (concatenación)
- ✅ Manejo de épsilon (ε)
- ✅ Guardado automático de imágenes
- ✅ Procesamiento por lotes de múltiples expresiones

## 📦 Dependencias

El proyecto requiere las siguientes librerías de Python:

```
matplotlib
numpy
```

## ⚙️ Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Vann06/Lab3_TCC.git
   cd Lab3_TCC
   ```

2. **Instala las dependencias:**
   ```bash
   pip install matplotlib numpy
   ```

## 🏃‍♂️ Uso

### Ejecución Principal

Para procesar todas las expresiones del archivo `expresiones_arbol.txt`:

```bash
python backtracking.py
```

### Ejecución del Algoritmo Shunting Yard

Para ver solo la conversión a notación postfija:

```bash
python shunting_yard.py
```

### Expresiones de Ejemplo

El archivo `expresiones_arbol.txt` contiene las siguientes expresiones:

```
(a* | b*)+
((ε | a) | b*)*
(a | b)* abb (a | b)*
0? (1?)? 0*
```

### Procesamiento de Expresiones Personalizadas

Puedes agregar tus propias expresiones regulares al archivo `expresiones_arbol.txt`, una por línea.

## 📁 Estructura de Salida

Al ejecutar el programa principal, se creará automáticamente una carpeta `arboles_sintacticos/` que contendrá:

```
arboles_sintacticos/
├── expresion_1_astarbostarplus.png
├── expresion_2_epsilonaobostarstar.png
├── expresion_3_aobostarabbabobostarstar.png
└── expresion_4_0opt1optopt0star.png
```

Cada imagen muestra:
- El árbol sintáctico visual
- La expresión original
- La notación postfija equivalente
- Leyenda distinguiendo operadores y operandos

## 🎨 Visualización

Los árboles generados utilizan:
- **Círculos morados**: Operadores (`*`, `+`, `?`, `|`, `.`)
- **Rectángulos azules**: Operandos (letras, números, `ε`)
- **Líneas negras**: Conexiones entre nodos

## 🔧 Operadores Soportados

| Operador | Nombre | Precedencia | Descripción |
|----------|---------|-------------|-------------|
| `*` | Estrella de Kleene | 3 | Cero o más repeticiones |
| `+` | Más | 3 | Una o más repeticiones |
| `?` | Interrogación | 3 | Cero o una repetición |
| `.` | Concatenación | 2 | Unión secuencial (implícita) |
| `|` | Alternancia | 1 | OR lógico |

## 🖥️ Ejemplo de Ejecución

```bash
C:\Users\Vianka\Documents\GitHub\Lab3_TCC> python backtracking.py

GENERADOR DE ARBOLES SINTACTICOS
==================================================
Archivo leido: expresiones_arbol.txt
Expresiones encontradas: 4
  1. '(a* | b*)+'
  2. '((ε | a) | b*)*'
  3. '(a | b)* abb (a | b)*'
  4. '0? (1?)? 0*'
------------------------------
Carpeta creada: arboles_sintacticos

PROCESANDO Expresion 1 de 4: '(a* | b*)+'
--------------------------------------------------
Construyendo arbol desde postfix: 'a*b*|+'
Postfix: a*b*|+
Arbol construido exitosamente
Árbol guardado como: arboles_sintacticos\expresion_1_astarbostarplus.png
EXITO: Expresion 1 completada

...

PROCESO COMPLETADO
TODOS LOS ARBOLES GUARDADOS EN: arboles_sintacticos
```

## 🐛 Solución de Problemas

### Error: Módulo no encontrado
```bash
pip install matplotlib numpy
```

### Error: Archivo no encontrado
Verifica que `expresiones_arbol.txt` existe en el directorio del proyecto.

### Error: No se generan imágenes
Asegúrate de tener permisos de escritura en el directorio del proyecto.

## 👥 Contribuciones

Este proyecto es parte del Lab3_TCC. Para contribuir:

1. Fork del repositorio
2. Crea una rama para tu feature
3. Commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo para el curso de Teoría de la Computación y Compiladores.

## 📞 Contacto

- **Repositorio**: [Lab3_TCC](https://github.com/Vann06/Lab3_TCC)
- **Rama actual**: ejercicio-1

---
