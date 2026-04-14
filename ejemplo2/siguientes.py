grammar = {
    'S': [['B', 'uno'], ['dos', 'C'], ['e']],
    'A': [['S', 'tres', 'B', 'C'], ['cuatro'], ['e']],
    'B': [['A', 'cinco', 'C', 'seis'], ['e']],
    'C': [['siete', 'B'], ['e']],
}

non_terminals = set(grammar.keys())
terminals = {'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete'}
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

print("EJERCICIO 2 - CONJUNTOS DE SIGUIENTES")

for nt in ['S', 'A', 'B', 'C']:
    print(f"  SIGUIENTES({nt}) = {{ {', '.join(sorted(siguientes[nt]))} }}")
print()
print("Notas de derivacion:")
print("  SIGUIENTES(S) = { $ } union SIGUIENTES(A) si S en A -> S tres B C")
print("                  = { $, tres } + lo que sigue a S en otras reglas")
print("  SIGUIENTES(C) = SIGUIENTES(A) cuando C es el ultimo de A -> S tres B C")
print("                  union SIGUIENTES(S) cuando C es el ultimo de S -> dos C")
print("  SIGUIENTES(B) = { cinco } desde A -> ... cinco, union SIGUIENTES de donde B aparece al final")
print("  SIGUIENTES(A) = { cinco } desde B -> A cinco C seis")
