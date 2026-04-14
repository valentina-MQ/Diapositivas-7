
grammar = {
    'S':  [['A', 'B', 'C'], ['D', 'E']],
    'A':  [['dos', 'B', 'tres'], ['e']],
    'B':  [["B'"]],
    "B'": [['cuatro', 'C', 'cinco', "B'"], ['e']],
    'C':  [['seis', 'A', 'B'], ['e']],
    'D':  [['uno', 'A', 'E'], ['B']],
    'E':  [['tres']],
}

non_terminals = set(grammar.keys())
terminals = {'dos', 'tres', 'cuatro', 'cinco', 'seis', 'uno'}
start_symbol = 'S'


#Los primeros
def compute_primeros(grammar, non_terminals):
    primeros = {nt: set() for nt in non_terminals}
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == ['e']:
                    if 'e' not in primeros[nt]:
                        primeros[nt].add('e')
                        changed = True
                else:
                    i = 0
                    while i < len(prod):
                        symbol = prod[i]
                        if symbol not in non_terminals:
                            if symbol not in primeros[nt]:
                                primeros[nt].add(symbol)
                                changed = True
                            break
                        else:
                            before = len(primeros[nt])
                            primeros[nt] |= (primeros[symbol] - {'e'})
                            if len(primeros[nt]) > before:
                                changed = True
                            if 'e' in primeros[symbol]:
                                i += 1
                            else:
                                break
                    else:
                        if 'e' not in primeros[nt]:
                            primeros[nt].add('e')
                            changed = True
    return primeros


#Los siguientes

def primeros_cadena(cadena, primeros, non_terminals):
    result = set()
    for symbol in cadena:
        if symbol == 'e':
            result.add('e')
            break
        if symbol not in non_terminals:
            result.add(symbol)
            break
        result |= (primeros[symbol] - {'e'})
        if 'e' not in primeros[symbol]:
            break
    else:
        result.add('e')
    return result


def compute_siguientes(grammar, non_terminals, primeros, start_symbol):
    siguientes = {nt: set() for nt in non_terminals}
    siguientes[start_symbol].add('$')
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == ['e']:
                    continue
                for i, symbol in enumerate(prod):
                    if symbol not in non_terminals:
                        continue
                    beta = prod[i+1:]
                    if beta:
                        prim_beta = primeros_cadena(beta, primeros, non_terminals)
                        before = len(siguientes[symbol])
                        siguientes[symbol] |= (prim_beta - {'e'})
                        if len(siguientes[symbol]) > before:
                            changed = True
                        if 'e' in prim_beta:
                            before = len(siguientes[symbol])
                            siguientes[symbol] |= siguientes[nt]
                            if len(siguientes[symbol]) > before:
                                changed = True
                    else:
                        before = len(siguientes[symbol])
                        siguientes[symbol] |= siguientes[nt]
                        if len(siguientes[symbol]) > before:
                            changed = True
    return siguientes


def compute_prediccion(grammar, non_terminals, primeros, siguientes):
    prediccion = {}
    for nt, productions in grammar.items():
        prediccion[nt] = []
        for prod in productions:
            if prod == ['e']:
                pred = set(siguientes[nt])
            else:
                prim = primeros_cadena(prod, primeros, non_terminals)
                pred = prim - {'e'}
                if 'e' in prim:
                    pred |= siguientes[nt]
            prediccion[nt].append((prod, pred))
    return prediccion


def check_ll1(prediccion):
    is_ll1 = True
    conflicts = []
    for nt, rules in prediccion.items():
        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                inter = rules[i][1] & rules[j][1]
                if inter:
                    is_ll1 = False
                    conflicts.append((nt, rules[i][0], rules[j][0], inter))
    return is_ll1, conflicts


primeros = compute_primeros(grammar, non_terminals)
siguientes = compute_siguientes(grammar, non_terminals, primeros, start_symbol)
prediccion = compute_prediccion(grammar, non_terminals, primeros, siguientes)
is_ll1, conflicts = check_ll1(prediccion)

print("EJERCICIO 1 - PREDICCION, LL(1) Y ASDR")

print("\n-- Conjuntos de PRIMEROS --")
for nt in ["S", "A", "B", "B'", "C", "D", "E"]:
    print(f"  PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")

print("\n-- Conjuntos de SIGUIENTES --")
for nt in ["S", "A", "B", "B'", "C", "D", "E"]:
    print(f"  SIGUIENTES({nt}) = {{ {', '.join(sorted(siguientes[nt]))} }}")

print("\n-- Conjuntos de PREDICCION --")
for nt in ["S", "A", "B", "B'", "C", "D", "E"]:
    for prod, pred in prediccion[nt]:
        prod_str = ' '.join(prod)
        print(f"  PRED({nt} -> {prod_str}) = {{ {', '.join(sorted(pred))} }}")

print(f"\n-- Verificacion LL(1) --")
if is_ll1:
    print("  La gramatica ES LL(1).")
    print("  No existen simbolos comunes en los conjuntos de prediccion")
    print("  de ninguna pareja de reglas del mismo no terminal.")
else:
    print("  La gramatica NO ES LL(1). Conflictos encontrados:")
    for nt, p1, p2, inter in conflicts:
        print(f"    {nt}: '{' '.join(p1)}' vs '{' '.join(p2)}' -> interseccion {{ {', '.join(sorted(inter))} }}")



print("\nASDR\n")

class ASDR_Ej1:
    def __init__(self, tokens):
        # tokens es una lista de terminales mas '$' al final
        self.tokens = tokens + ['$']
        self.pos = 0

    def token(self):
        return self.tokens[self.pos]

    def emparejar(self, esperado):
        if self.token() == esperado:
            self.pos += 1
        else:
            raise SyntaxError(
                f"Error sintactico: se esperaba '{esperado}' pero se encontro '{self.token()}'"
            )

    def S(self):
        t = self.token()

        pred_abc = prediccion['S'][0][1]
        pred_de  = prediccion['S'][1][1]
        if t in pred_abc and t not in pred_de:
            self.A(); self.B(); self.C()
        elif t in pred_de and t not in pred_abc:
            self.D(); self.E()
        elif t in pred_abc:
            self.A(); self.B(); self.C()
        else:
            raise SyntaxError(f"Error en S: token inesperado '{t}'")

    def A(self):
        t = self.token()
        if t == 'dos':
            self.emparejar('dos'); self.B(); self.emparejar('tres')
        elif t in prediccion['A'][1][1]:
            pass  #epsilon
        else:
            raise SyntaxError(f"Error en A: token inesperado '{t}'")

    def B(self):
        self.Bp()  #B -> B'

    def Bp(self):
        t = self.token()
        if t == 'cuatro':
            self.emparejar('cuatro'); self.C(); self.emparejar('cinco'); self.Bp()
        elif t in prediccion["B'"][1][1]:
            pass  #epsilon
        else:
            raise SyntaxError(f"Error en B': token inesperado '{t}'")

    def C(self):
        t = self.token()
        if t == 'seis':
            self.emparejar('seis'); self.A(); self.B()
        elif t in prediccion['C'][1][1]:
            pass  #epsilon
        else:
            raise SyntaxError(f"Error en C: token inesperado '{t}'")

    def D(self):
        t = self.token()
        if t == 'uno':
            self.emparejar('uno'); self.A(); self.E()
        elif t in prediccion['D'][1][1]:
            self.B()
        else:
            raise SyntaxError(f"Error en D: token inesperado '{t}'")

    def E(self):
        t = self.token()
        if t == 'tres':
            self.emparejar('tres')
        else:
            raise SyntaxError(f"Error en E: token inesperado '{t}'")

    def parse(self):
        self.S()
        if self.token() != '$':
            raise SyntaxError(f"Error: entrada no consumida completamente, token '{self.token()}'")
        print("  Cadena aceptada.")


casos = [
    [],                               
    ['tres'],                           
    ['dos', 'tres'],                    
    ['uno', 'tres', 'tres'],           
    ['seis', 'tres'],                   
]

for caso in casos:
    parser = ASDR_Ej1(caso)
    entrada = ' '.join(caso)
    try:
        parser.parse()
        print(f"  Entrada [ {entrada} ] -> ACEPTADA")
    except SyntaxError as e:
        print(f"  Entrada [ {entrada} ] -> RECHAZADA: {e}")
