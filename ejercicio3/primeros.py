grammar = {
    'S':  [['A', 'B', 'C', "S'"]],
    "S'": [['uno', "S'"], ['e']],
    'A':  [['dos', 'B', 'C'], ['e']],
    'B':  [['C', 'tres'], ['e']],
    'C':  [['cuatro', 'B'], ['e']],
}

non_terminals = set(grammar.keys())
terminals = {'uno', 'dos', 'tres', 'cuatro'}


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


primeros = compute_primeros(grammar, non_terminals)

print("EJERCICIO 3 - CONJUNTOS DE PRIMEROS")
print("Gramatica sin recursividad por la izquierda")

for nt in ["S", "S'", "A", "B", "C"]:
    print(f"  PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")
print()
print("Derivacion:")
print("  PRIMEROS(C)  = { cuatro, e }")
print("  PRIMEROS(B)  = { PRIMEROS(C) - e } union { e } = { cuatro, e }")
print("                 (C puede derivar epsilon, luego toma 'tres'; B -> e tambien)")
print("  PRIMEROS(A)  = { dos, e }  (A -> dos B C | e)")
print("  PRIMEROS(S') = { uno, e }  (S' -> uno S' | e)")
print("  PRIMEROS(S)  = PRIMEROS(A B C S')")
print("               = { dos } union { cuatro, e } ... = { dos, cuatro, tres, e }")
