class Grammar:
    def __init__(self, non_terminals=None, terminals=None, productions=None, start_symbol=None):
        self.non_terminals = set(non_terminals) if non_terminals else set()
        self.terminals = set(terminals) if terminals else set()
        self.productions = productions or {}
        self.start_symbol = start_symbol
    
    def __str__(self):
        result = f"Non-terminals: {', '.join(sorted(self.non_terminals))}\n"
        result += f"Terminals: {', '.join(sorted(self.terminals))}\n"
        result += f"Start symbol: {self.start_symbol}\n"
        result += "Productions:\n"
        for nt in sorted(self.non_terminals):
            if nt in self.productions and self.productions[nt]:
                for prod in sorted(self.productions[nt]):
                    result += f"  {nt} -> {prod}\n"
        return result

    @classmethod
    def from_variant_1(cls):
        """Create a Grammar instance using the variant 1 data"""
        non_terminals = {'S', 'A', 'B', 'C', 'D', 'E'}
        terminals = {'a', 'b'}
        productions = {
            'S': ['aB', 'AC'],
            'A': ['a', 'ASC', 'BC', 'aD'],
            'B': ['b', 'bS'],
            'C': ['ε', 'BA'],
            'D': ['abC'],
            'E': ['aB']
        }
        return cls(non_terminals, terminals, productions, 'S')

    @classmethod
    def parse_grammar(cls, grammar_string):
        """Parse a grammar from a string representation"""
        lines = grammar_string.strip().split('\n')
        non_terminals = set()
        terminals = set()
        productions = {}
        start_symbol = None
        
        for line in lines:
            if '->' in line:
                left, right = line.split('->')
                left = left.strip()
                right = right.strip()
                
                if not start_symbol:
                    start_symbol = left
                
                non_terminals.add(left)
                
                if left not in productions:
                    productions[left] = []
                
                productions[left].append(right)
                
                for char in right:
                    if char.islower() or char in "ε":
                        terminals.add(char)
        
        # Remove epsilon from terminals if present
        if 'ε' in terminals:
            terminals.remove('ε')
            
        return cls(non_terminals, terminals, productions, start_symbol)

def convert_to_cnf_variant_1(grammar):
    """Convert a grammar to Chomsky Normal Form using Variant 1 approach"""
    print("\nStep 1: Eliminate ε-productions")
    new_grammar = eliminate_epsilon_productions(grammar)
    print(new_grammar)
    
    print("\nStep 2: Eliminate renaming productions (A -> B)")
    new_grammar = eliminate_renaming_productions(new_grammar)
    print(new_grammar)
    
    print("\nStep 3: Eliminate inaccessible symbols")
    new_grammar = eliminate_inaccessible_symbols(new_grammar)
    print(new_grammar)
    
    print("\nStep 4: Eliminate non-productive symbols")
    new_grammar = eliminate_non_productive_symbols(new_grammar)
    print(new_grammar)
    
    print("\nStep 5: Obtain the Chomsky Normal Form")
    new_grammar = convert_to_cnf_final(new_grammar)
    print(new_grammar)
    
    return new_grammar

def eliminate_epsilon_productions(grammar):
    """Eliminate ε-productions from the grammar"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Find all nullable non-terminals (those that can derive ε)
    nullable = set()
    
    # First pass: Find directly nullable non-terminals
    for nt, prods in new_grammar.productions.items():
        if 'ε' in prods:
            nullable.add(nt)
            prods.remove('ε')
            print(f"Found directly nullable non-terminal: {nt}")
    
    # Find all indirectly nullable non-terminals until no new ones are found
    changed = True
    while changed:
        changed = False
        for nt, prods in new_grammar.productions.items():
            if nt not in nullable:
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        nullable.add(nt)
                        changed = True
                        print(f"Found indirectly nullable non-terminal: {nt}")
                        break
    
    print(f"All nullable non-terminals: {nullable}")
    
    # For each production, generate new ones by removing nullable symbols
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = prods.copy()
        for prod in prods:
            # Find positions of nullable symbols
            nullable_positions = [i for i, symbol in enumerate(prod) if symbol in nullable]
            
            # Generate all possible combinations of removing nullable symbols
            # (except removing all of them which would create an ε-production)
            for mask in range(1, 2**len(nullable_positions)):
                positions_to_remove = [nullable_positions[i] 
                                      for i in range(len(nullable_positions)) 
                                      if (mask & (1 << i))]
                
                new_prod = ''.join(symbol for i, symbol in enumerate(prod) 
                                  if i not in positions_to_remove)
                
                # Don't add empty string unless it's for the start symbol and it's nullable
                if new_prod and new_prod not in new_prods:
                    new_prods.append(new_prod)
                    print(f"Added new production: {nt} -> {new_prod}")
        
        new_grammar.productions[nt] = new_prods
    
    # Special case: if the start symbol is nullable and should produce ε
    if new_grammar.start_symbol in nullable and all(len(prod) > 0 for prod in new_grammar.productions[new_grammar.start_symbol]):
        # Only add ε if the start symbol can't already derive it through other means
        can_derive_epsilon = False
        for prod in new_grammar.productions[new_grammar.start_symbol]:
            if all(symbol in nullable for symbol in prod):
                can_derive_epsilon = True
                break
        
        if not can_derive_epsilon:
            new_grammar.productions[new_grammar.start_symbol].append('ε')
            print(f"Added ε-production for start symbol: {new_grammar.start_symbol} -> ε")
    
    return new_grammar

def eliminate_renaming_productions(grammar):
    """Eliminate renaming productions (A -> B where B is a non-terminal)"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Find all pairs (A, B) where A -> B directly
    direct_pairs = []
    for nt, prods in new_grammar.productions.items():
        for prod in prods:
            if len(prod) == 1 and prod in new_grammar.non_terminals:
                direct_pairs.append((nt, prod))
                print(f"Found direct renaming: {nt} -> {prod}")
    
    # Compute the transitive closure of renaming
    renaming_pairs = direct_pairs.copy()
    changed = True
    while changed:
        changed = False
        for a, b in list(renaming_pairs):
            for c, d in list(renaming_pairs):
                if b == c and (a, d) not in renaming_pairs:
                    renaming_pairs.append((a, d))
                    changed = True
                    print(f"Found indirect renaming: {a} -> {d}")
    
    print(f"All renaming pairs: {renaming_pairs}")
    
    # Replace renaming productions
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = [p for p in prods if not (len(p) == 1 and p in new_grammar.non_terminals)]
        
        for a, b in renaming_pairs:
            if a == nt and b in new_grammar.productions:
                for prod in new_grammar.productions[b]:
                    if len(prod) != 1 or prod not in new_grammar.non_terminals:
                        if prod not in new_prods:
                            new_prods.append(prod)
                            print(f"Added production from renaming: {a} -> {prod}")
        
        new_grammar.productions[nt] = new_prods
    
    return new_grammar

def eliminate_inaccessible_symbols(grammar):
    """Eliminate inaccessible symbols (symbols that can't be reached from the start symbol)"""
    new_grammar = Grammar(
        set(),  # Will be populated with accessible non-terminals
        set(),  # Will be populated with accessible terminals
        {},     # Will be populated with productions of accessible symbols
        grammar.start_symbol
    )
    
    # Find accessible symbols using breadth-first search
    accessible = set([grammar.start_symbol])
    queue = [grammar.start_symbol]
    
    while queue:
        current = queue.pop(0)
        
        if current in grammar.productions:
            for prod in grammar.productions[current]:
                for symbol in prod:
                    if symbol in grammar.non_terminals and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)
                    elif symbol in grammar.terminals:
                        new_grammar.terminals.add(symbol)
    
    print(f"Accessible symbols: {accessible}")
    
    # Create new grammar with only accessible symbols
    new_grammar.non_terminals = accessible
    for nt in accessible:
        if nt in grammar.productions:
            new_grammar.productions[nt] = grammar.productions[nt].copy()
    
    # Remove any productions that reference inaccessible symbols
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = []
        for prod in prods:
            valid = True
            for symbol in prod:
                if symbol in grammar.non_terminals and symbol not in accessible:
                    valid = False
                    break
            if valid:
                new_prods.append(prod)
            else:
                print(f"Removed production with inaccessible symbol: {nt} -> {prod}")
        
        new_grammar.productions[nt] = new_prods
    
    return new_grammar

def eliminate_non_productive_symbols(grammar):
    """Eliminate non-productive symbols (symbols that don't derive terminal strings)"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Find productive symbols
    productive = set()
    
    # First pass: Find directly productive non-terminals
    for nt, prods in new_grammar.productions.items():
        for prod in prods:
            if all(symbol in new_grammar.terminals for symbol in prod):
                productive.add(nt)
                print(f"Found directly productive non-terminal: {nt}")
                break
    
    # Find all indirectly productive non-terminals until no new ones are found
    changed = True
    while changed:
        changed = False
        for nt, prods in new_grammar.productions.items():
            if nt not in productive:
                for prod in prods:
                    if all(symbol in productive or symbol in new_grammar.terminals for symbol in prod):
                        productive.add(nt)
                        changed = True
                        print(f"Found indirectly productive non-terminal: {nt}")
                        break
    
    print(f"Productive symbols: {productive}")
    
    # Remove non-productive symbols from non-terminals
    new_non_terminals = set()
    new_productions = {}
    
    for nt in productive:
        new_non_terminals.add(nt)
        new_productions[nt] = []
        
        if nt in new_grammar.productions:
            for prod in new_grammar.productions[nt]:
                if all(symbol in productive or symbol in new_grammar.terminals for symbol in prod):
                    new_productions[nt].append(prod)
                else:
                    print(f"Removed production with non-productive symbol: {nt} -> {prod}")
    
    # Update grammar
    new_grammar.non_terminals = new_non_terminals
    new_grammar.productions = new_productions
    
    return new_grammar

def convert_to_cnf_final(grammar):
    """Convert grammar to Chomsky Normal Form (A -> BC or A -> a)"""
    new_grammar = Grammar(
        grammar.non_terminals.copy(),
        grammar.terminals.copy(),
        {nt: prods.copy() for nt, prods in grammar.productions.items()},
        grammar.start_symbol
    )
    
    # Step 1: Replace terminal symbols in long productions
    terminal_to_nt = {}
    next_nt_index = 1
    
    # Create mapping for terminals
    for terminal in grammar.terminals:
        nt_name = f"T_{terminal}"
        # Ensure uniqueness
        while nt_name in new_grammar.non_terminals:
            nt_name = f"T_{next_nt_index}_{terminal}"
            next_nt_index += 1
        
        terminal_to_nt[terminal] = nt_name
        new_grammar.non_terminals.add(nt_name)
        new_grammar.productions[nt_name] = [terminal]
        print(f"Created terminal-to-nonterminal mapping: {nt_name} -> {terminal}")
    
    # Replace terminals in long productions
    for nt, prods in list(new_grammar.productions.items()):
        new_prods = []
        for prod in prods:
            if len(prod) > 1:
                new_prod = ""
                for symbol in prod:
                    if symbol in grammar.terminals:
                        new_prod += terminal_to_nt[symbol]
                    else:
                        new_prod += symbol
                new_prods.append(new_prod)
                print(f"Replaced terminals in long production: {nt} -> {prod} becomes {nt} -> {new_prod}")
            else:
                new_prods.append(prod)
        new_grammar.productions[nt] = new_prods
    
    # Step 2: Break down productions with more than 2 symbols
    next_new_var = 1
    final_productions = {}
    
    for nt, prods in new_grammar.productions.items():
        final_productions[nt] = []
        
        for prod in prods:
            if len(prod) <= 2:
                # Keep productions with 1 or 2 symbols
                final_productions[nt].append(prod)
            else:
                # Break down productions with more than 2 symbols
                print(f"Breaking down: {nt} -> {prod}")
                
                # Create a new non-terminal for the first two symbols
                first_nt = nt
                symbols = list(prod)
                
                for i in range(0, len(symbols) - 2):
                    new_var = f"X_{next_new_var}"
                    next_new_var += 1
                    
                    # Ensure uniqueness
                    while new_var in new_grammar.non_terminals:
                        new_var = f"X_{next_new_var}"
                        next_new_var += 1
                    
                    new_grammar.non_terminals.add(new_var)
                    
                    if i == 0:
                        final_productions[first_nt].append(symbols[i] + new_var)
                        print(f"  Added: {first_nt} -> {symbols[i]}{new_var}")
                    else:
                        if prev_var not in final_productions:
                            final_productions[prev_var] = []
                        final_productions[prev_var].append(symbols[i] + new_var)
                        print(f"  Added: {prev_var} -> {symbols[i]}{new_var}")
                    
                    prev_var = new_var
                
                # Add the last production
                if prev_var not in final_productions:
                    final_productions[prev_var] = []
                final_productions[prev_var].append(symbols[-2] + symbols[-1])
                print(f"  Added: {prev_var} -> {symbols[-2]}{symbols[-1]}")
    
    # Update grammar with final productions
    new_grammar.productions = final_productions
    
    return new_grammar

def main():
    print("Chomsky Normal Form Converter - Variant 1")
    print("----------------------------------------\n")
    
    # Get grammar from variant 1
    grammar = Grammar.from_variant_1()
    print("Original Grammar:")
    print(grammar)
    
    # Convert to CNF using variant 1 approach
    cnf_grammar = convert_to_cnf_variant_1(grammar)
    print("\nFinal Grammar in Chomsky Normal Form:")
    print(cnf_grammar)
    
    # BONUS: Allowing any input grammar
    print("\nBonus: Convert a custom grammar to CNF")
    print("Enter your grammar in the format 'A -> aBc' (one production per line).")
    print("Enter a blank line to finish input.")
    
    custom_grammar_str = ""
    while True:
        line = input()
        if not line:
            break
        custom_grammar_str += line + "\n"
    
    if custom_grammar_str:
        try:
            custom_grammar = Grammar.parse_grammar(custom_grammar_str)
            print("\nCustom Grammar:")
            print(custom_grammar)
            
            cnf_custom_grammar = convert_to_cnf_variant_1(custom_grammar)
            print("\nCustom Grammar in Chomsky Normal Form:")
            print(cnf_custom_grammar)
        except Exception as e:
            print(f"Error processing custom grammar: {e}")

if __name__ == "__main__":
    main()
