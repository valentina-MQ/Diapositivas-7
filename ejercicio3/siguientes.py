grammar = {
    'S':  [['A', 'B', 'C', "S'"]],
    "S'": [['uno', "S'"], ['e']],
    'A':  [['dos', 'B', 'C'], ['e']],
    'B':  [['C', 'tres'], ['e']],
    'C':  [['cuatro', 'B'], ['e']],
}

non_terminals = set(grammar.keys())
terminals = {'uno', 'dos', 'tres', 'cuatro'}
start_symbol = 'S'


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


primeros = compute_primeros(grammar, non_terminals)
siguientes = compute_siguientes(grammar, non_terminals, primeros, start_symbol)

print("EJERCICIO 3 - CONJUNTOS DE SIGUIENTES")
print("Gramatica sin recursividad por la izquierda")

for nt in ["S", "S'", "A", "B", "C"]:
    print(f"  SIGUIENTES({nt}) = {{ {', '.join(sorted(siguientes[nt]))} }}")
print()
print("Notas:")
print("  SIGUIENTES(S)  = { $ }")
print("  SIGUIENTES(S') = SIGUIENTES(S) union SIGUIENTES(S') = { $ }")
print("  SIGUIENTES(A)  = PRIMEROS(B C S') - {e} union SIGUIENTES(S)")
print("  SIGUIENTES(B)  = PRIMEROS(C S') - {e} union ... union { tres }")
print("  SIGUIENTES(C)  = PRIMEROS(S') - {e} union SIGUIENTES(S) union { tres } ...")
