import sys
import networkx as nx

# Función para leer el archivo de gramática validando
def leer_gramatica_validando(archivo):
    reglas = {}
    terminales = set()  # Usamos sets para evitar duplicados
    no_terminales = set()

    try:
        with open(archivo, 'r') as f:
            lineas_validas = 0

            # Primera pasada para identificar todos los no terminales
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue  # Ignorar líneas vacías o comentarios
                if linea.count('->') != 1:
                    print(f"Error: La línea '{linea}' tiene más de un '->' o está malformada.")
                    continue

                lado_izq, _ = linea.split('->')
                lado_izq = lado_izq.strip()
                no_terminales.add(lado_izq)  # Añadir al conjunto de no terminales

            # Segunda pasada para procesar las reglas
            f.seek(0)  # Reiniciar el puntero del archivo al principio
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue  # Ignorar líneas vacías o comentarios

                lado_izq, lado_der = linea.split('->')
                lado_izq = lado_izq.strip()
                producciones = lado_der.strip().split('|')  # Separar las alternativas con '|'

                if lado_izq not in reglas:
                    reglas[lado_izq] = []

                for produccion in producciones:
                    simbolos = produccion.strip().split()

                    # Validar paréntesis en la producción
                    paren_abiertos = simbolos.count('(')
                    paren_cerrados = simbolos.count(')')
                    if paren_abiertos != paren_cerrados:
                        print(f"Error: La producción '{produccion.strip()}' tiene un número desbalanceado de paréntesis.")
                        continue

                    reglas[lado_izq].append(simbolos)

                    # Clasificar terminales
                    for simbolo in simbolos:
                        if simbolo not in no_terminales and simbolo != 'ε':
                            terminales.add(simbolo)

                lineas_validas += 1

            if lineas_validas == 0:
                print(f"Error: El archivo '{archivo}' no contiene reglas gramaticales válidas.")
                sys.exit(1)

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no se encontró.")
        sys.exit(1)

    return reglas, sorted(terminales), sorted(no_terminales)

def generar_arbol_frase(G, reglas, frase, simbolo, padre=None, frase_actual=None, profundidad=0, limite_profundidad=1000, nodo_id=[0]):
    if frase_actual is None:
        frase_actual = []

    if profundidad > limite_profundidad:
        print(f"Excedido el límite de profundidad ({limite_profundidad})")
        return False

    if len(frase_actual) == len(frase):
        return frase_actual == frase

    nodo_id[0] += 1
    nodo_actual = f"{simbolo}_{nodo_id[0]}"
    G.add_node(nodo_actual, label=simbolo)
    if padre:
        G.add_edge(padre, nodo_actual)

    if simbolo in reglas:
        for produccion in reglas[simbolo]:
            nueva_frase_actual = frase_actual.copy()
            simbolos_expandidos = True

            for sub_simbolo in produccion:
                if sub_simbolo == 'ε':
                    continue

                if len(nueva_frase_actual) < len(frase):
                    if sub_simbolo not in reglas and sub_simbolo != frase[len(nueva_frase_actual)]:
                        simbolos_expandidos = False
                        break

                if not generar_arbol_frase(G, reglas, frase, sub_simbolo, nodo_actual, nueva_frase_actual, profundidad + 1, limite_profundidad, nodo_id):
                    simbolos_expandidos = False
                    break

            if simbolos_expandidos:
                frase_actual[:] = nueva_frase_actual
                return True

    else:
        if len(frase_actual) < len(frase) and simbolo == frase[len(frase_actual)]:
            frase_actual.append(simbolo)
            return True

    return False




# Función para visualizar el árbol
def visualizar_arbol(G):
    A = nx.nx_agraph.to_agraph(G)
    A.layout('dot')  # Usar el layout 'dot' para obtener una forma de árbol
    A.draw('arbol_frase.png')  # Guardar el gráfico en un archivo PNG
    print("El árbol ha sido guardado como 'arbol_frase.png'")


# Programa principal
def main():
    archivo_gramatica = 'gramatica.txt'  # Archivo por defecto
    frase = []  # Aquí va la frase a derivar

    if len(sys.argv) > 1:
        archivo_gramatica = sys.argv[1]
        frase = sys.argv[2:]  # Frase a derivar pasada como argumentos

    if not frase:
        print("Por favor, ingresa una frase para derivar.")
        sys.exit(1)

    # Si la frase está entre comillas, la unimos
    frase = ' '.join(frase).strip('"').split()  # Une y separa por espacios

    try:
        reglas, terminales, no_terminales = leer_gramatica_validando(archivo_gramatica)
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_gramatica}' no se encontró.")
        sys.exit(1)

    G = nx.DiGraph()
    nodo_id = [0]  # Inicializar nodo_id como una lista

    # Obtener el primer símbolo del archivo como símbolo inicial
    simbolo_inicial = next(iter(reglas.keys()))  # Primer símbolo de las reglas

    # Generar árbol de derivación para la frase
    if not generar_arbol_frase(G, reglas, frase, simbolo_inicial, nodo_id=nodo_id):
        print(f"La frase {' '.join(frase)} no puede ser derivada de la gramática.")
    else:
        visualizar_arbol(G)

    # Imprimir terminales y no terminales
    print(f"Terminales: {terminales}")
    print(f"No terminales: {no_terminales}")

if __name__ == "__main__":  
    main()