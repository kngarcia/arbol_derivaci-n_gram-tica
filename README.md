# Árbol de Derivación & Gramáticas en Python

## Integrantes del grupo:
  - Camilo López
  - Juan Josá Márquez
  - Kevin García
  - Miguel Fernández

# Generador de Árboles de Derivación a partir de Gramáticas

Este proyecto es una herramienta en Python que permite leer gramáticas desde un archivo, validar la sintaxis de la gramática, y generar un árbol de derivación para una frase específica basada en las reglas definidas. Usa la librería `networkx` para la representación gráfica del árbol y `pygraphviz` para la visualización.

## Requisitos

- Python 3.12.3
- Librerías:
    - `networkx`
    - `pygraphviz`

Puedes instalarlas ejecutando:

```bash
sudo apt-get install graphviz graphviz-dev
```


```bash
pip install networkx pygraphviz
```

## Configuración del Entorno
Virtual Environment (opcional pero recomendado)
Es recomendable crear un entorno virtual para evitar conflictos de dependencias. Puedes crear y activar un entorno virtual usando los siguientes comandos:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Estructura del Proyecto

`main.py`: Archivo principal que contiene la lógica del generador de árboles sintácticos.
`gramatica(2).txt`: Archivo de texto que define las reglas de la gramática utilizada.
`arbol_frase.png`: Imagen generada del árbol sintáctico (se generará al ejecutar el script).

## Funcionalidades

### 1. Lectura y Validación de Gramática

La función `leer_gramatica_validando(archivo)` lee un archivo de texto que contiene reglas de gramática en formato:

```css
E  -> T E'
E' -> + T E' | - T E' | ε
T  -> F T'
T' -> * F T' | / F T' | ^ F T' | ε
F  -> id | num | ( E )
```

- Soporta reglas con alternativas separadas por `|`.
- Identifica y valida los no terminales (por el lado izquierdo de las reglas) y terminales (por el lado derecho).
- El archivo también puede contener comentarios, que deben empezar con `#`.

### 2. Generación del Árbol de Derivación

La función `generar_arbol_frase(G, reglas, frase, simbolo, ...)` genera un árbol de derivación que representa cómo se expande una frase a partir de un símbolo inicial de la gramática.

- Crea un nodo para cada símbolo no terminal que se expande.
- Intenta derivar la frase ingresada y crea el árbol correspondiente en un objeto de grafo dirigido `networkx.DiGraph`.

### 3. Visualización del Árbol

La función `visualizar_arbol(G)` dibuja y guarda el árbol de derivación generado en un archivo PNG (`arbol_frase.png`) usando `matplotlib`.

### 4. Programa Principal

El programa principal se ejecuta desde la línea de comandos. Lee el archivo de gramática y la frase que debe derivar. Si la frase es derivable, genera y guarda el árbol.

## Uso

### Ejecución del Programa

Debes ejecutar el programa desde la línea de comandos, especificando el archivo de gramática y la frase a derivar como argumentos:

```bash
python script.py gramatica.txt "frase_a_derivar"
```

#### Ejemplo:

```bash
python script.py gramatica.txt "id + id"
```
La frase debe ir entre comillas dobles `("")` o simples `('')`. Cada simbolo debe ir espaciado, es decir, si se quiere probar
la gramática del archivo `gramatica2.txt` que acepta frases con parentesis `()` este debe ser pasado como argumento de la siguiente 
forma: `"( id + (id * num) )"`

Si no se pasa una frase, el programa dará un error y pedirá que se ingrese una frase.

### Estructura del Archivo de Gramática

El archivo de gramática debe estar en el siguiente formato:

- Cada regla debe seguir el patrón `NoTerminal -> Producción1 | Producción2`.
- Los símbolos de una producción deben estar separados por espacios.
- Puedes incluir comentarios iniciados por `#`.

#### Ejemplo de gramática:

```css
S -> A B | C
A -> a
B -> b
C -> c
```

## Salida

- Si la frase es derivable, el programa generará un archivo `arbol_frase.png` con la representación del árbol de derivación.
- Si la frase no puede derivarse, se indicará en la consola.
- También se imprimen en la consola los terminales y no terminales de la gramática procesada.

### Ejemplo de Salida

En caso de éxito, se generará un archivo PNG que contiene el árbol de derivación de la frase ingresada. La consola imprimirá algo como:

```
Frase generada: ['b', 'c'] (Simbolo: S)
El árbol ha sido guardado como 'arbol_frase.png'
Terminales: ['a', 'b', 'c']
No terminales: ['A', 'B', 'C', 'S']
```

## Manejo de Errores

- El programa valida que las reglas de la gramática estén bien formadas, es decir, que tengan exactamente un símbolo `->`.
- Si el archivo no contiene reglas válidas o si la frase no es derivable, el programa emitirá mensajes de error apropiados.

## Notas

La recursión está limitada a un valor predeterminado (`limite_profundidad=1000`) para evitar loops infinitos en gramáticas recursivas.
