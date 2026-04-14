grammar = {
    'S': [['B', 'uno'], ['dos', 'C'], ['e']],
    'A': [['S', 'tres', 'B', 'C'], ['cuatro'], ['e']],
    'B': [['A', 'cinco', 'C', 'seis'], ['e']],
    'C': [['siete', 'B'], ['e']],
}

non_terminals = set(grammar.keys())
terminals = {'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete'}


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

print("EJERCICIO 2 - CONJUNTOS DE PRIMEROS")

for nt in ['S', 'A', 'B', 'C']:
    print(f"  PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")
print()
print("Derivacion de los resultados:")
print("  PRIMEROS(C) = { siete, e }")
print("  PRIMEROS(B) = { PRIMEROS(A) - e } union { e } = { cuatro, siete, uno, dos, e }")
print("                (A puede derivar epsilon, B -> e tambien)")
print("  PRIMEROS(A) = { PRIMEROS(S) - e } union { cuatro, e }")
print("              = { uno, dos, cuatro, e } union { PRIMEROS(B) si S deriva e }")
print("  PRIMEROS(S) = { PRIMEROS(B) - e } union { dos } union { e }")
print("              = { cuatro, siete, uno, dos, e }")
