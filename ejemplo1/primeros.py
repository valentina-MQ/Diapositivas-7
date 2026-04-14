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
                            #Es terminal
                            if symbol not in primeros[nt]:
                                primeros[nt].add(symbol)
                                changed = True
                            break
                        else:
                            #Es no terminal
                            before = len(primeros[nt])
                            primeros[nt] |= (primeros[symbol] - {'e'})
                            if len(primeros[nt]) > before:
                                changed = True
                            if 'e' in primeros[symbol]:
                                i += 1
                            else:
                                break
                    else:
                        #Todos los simbolos derivan epsilon
                        if 'e' not in primeros[nt]:
                            primeros[nt].add('e')
                            changed = True
    return primeros


primeros = compute_primeros(grammar, non_terminals)

print("EJERCICIO 1 - CONJUNTOS DE PRIMEROS")
print("Gramatica sin recursividad por la izquierda")
for nt in ["S", "A", "B", "B'", "C", "D", "E"]:
    print(f"  PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")
print()
print("Verificacion manual esperada:")
print("  PRIMEROS(E)  = { tres }")
print("  PRIMEROS(B') = { cuatro, e }")
print("  PRIMEROS(B)  = { cuatro, e }  (hereda de B')")
print("  PRIMEROS(A)  = { dos, e }")
print("  PRIMEROS(C)  = { seis, e }")
print("  PRIMEROS(D)  = { uno, cuatro, e }  (uno | PRIMEROS(B))")
print("  PRIMEROS(S)  = { dos, cuatro, seis, uno, tres, e }")
print("                  (PRIMEROS(A) + PRIMEROS(B) + PRIMEROS(C) + PRIMEROS(D))")
