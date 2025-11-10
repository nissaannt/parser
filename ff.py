
def compute_first(grammar):
    first = {}
    # Initialize FIRST sets
    for lhs, rhs in grammar:
        if lhs not in first:
            first[lhs] = set()

        for ch in rhs:
            if not ch.isupper():        # terminal
                first[ch] = {ch}
            else:                       # non-terminal
                if ch not in first:
                    first[ch] = set()

    # Compute FIRST iteratively
    for _ in range(1000):
        for lhs, rhs in grammar:
            for i, ch in enumerate(rhs):

                # Terminal → FIRST is itself
                if not ch.isupper(): first[lhs].add(ch) ; break
                    # first[lhs].add(ch)
                    # break

                # Non-terminal → add FIRST(ch) minus epsilon
                first[lhs].update(first[ch] - {'#'})

                # If ch cannot produce epsilon, stop
                if '#' not in first[ch]: break
                    # break

                # If last symbol and epsilon present → add epsilon
                if i == len(rhs) - 1: first[lhs].add('#')
                    # first[lhs].add('#')

    return first


def compute_follow(grammar, first):
    follow = {}

    # Initialize FOLLOW sets for all non-terminals
    for lhs, rhs in grammar:
        follow[lhs] = set()

    # Add $ to FOLLOW(start symbol)
    start_symbol = grammar[0][0]
    follow[start_symbol].add('$')

    # Iterative computation
    for _ in range(1000):
        for lhs, rhs in grammar:
            for i, ch in enumerate(rhs):
                if ch.isupper():  # Only non-terminals

                    # Consider the suffix after ch
                    suffix = rhs[i+1:]

                    # Compute FIRST(suffix)
                    first_of_suffix = set()
                    if suffix:
                        for sym in suffix:
                            first_of_suffix.update(first[sym] - {'#'})
                            if '#' not in first[sym]:
                                break
                        else:
                            # entire suffix can derive epsilon
                            first_of_suffix.add('#')

                        # Add FIRST(suffix) \ {e} to FOLLOW(ch)
                        follow[ch].update(first_of_suffix - {'#'})
                    else:
                        # No suffix, so just add FOLLOW(lhs)
                        first_of_suffix = {'#'}

                    # If suffix can produce epsilon, add FOLLOW(lhs)
                    if '#' in first_of_suffix:
                        follow[ch].update(follow[lhs])

    return follow



grammar = [
    ['S', 'BaDh'],
    ['B', 'cC'],
    ['C', 'bC'],
    ['C', '#'],
    ['D', 'EF'],
    ['E', 'g'],
    ['E', '#'],
    ['F', 'f'],
    ['F', '#']
]


first_sets = compute_first(grammar)
follow_sets = compute_follow(grammar, first_sets)


print("FIRST sets:")
for lhs in first_sets:
    if lhs.isupper(): 
        print(f"{lhs}: {first_sets[lhs]}")

print("\nFOLLOW sets:")
for lhs in follow_sets:
    print(f"{lhs}: {follow_sets[lhs]}")
