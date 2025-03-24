import random
import json
from functools import reduce
from collections import defaultdict

def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)

def string_belongs_to_language(config, input_string):
    delta, q0, F = config["delta"], config["q0"], set(config["F"])
    
    final_state = reduce(
        lambda state, symbol: delta.get(state, {}).get(symbol, None),
        input_string,
        q0
    )
    
    return final_state in F if final_state else False

def generate_from_non_terminal(production, vt, non_terminal):
    if non_terminal not in production:
        return ""
    
    return ''.join(
        symbol if symbol in vt else generate_from_non_terminal(production, vt, symbol)
        for symbol in random.choice(production[non_terminal])
    )

def generate_string(config):
    return generate_from_non_terminal(config["production"], set(config["vt"]), config["start_symbol"])

def ndfa_to_dfa(ndfa):
    Q, sigma, delta, q0, F = ndfa

    # Initialize DFA components
    dfa = defaultdict(dict)  # Transition table for DFA
    dfa_states = []  # List of DFA states (sets of NDFA states)
    dfa_final = set()  # Final states of DFA

    # Start state of DFA is a frozenset containing just the start state of the NDFA
    start_state = frozenset([q0])
    dfa_states.append(start_state)
    if start_state & F:
        dfa_final.add(start_state)

    # Mapping from NDFA state sets to DFA state indices
    state_map = {start_state: 0}
    unprocessed_states = [start_state]  # States to process

    while unprocessed_states:
        current_state = unprocessed_states.pop()

        for symbol in sigma:
            # Get the new set of states after the symbol transition
            next_state = frozenset([q for s in current_state for q in delta[s].get(symbol, [])])

            if next_state:
                if next_state not in state_map:
                    # Add new state to DFA
                    state_map[next_state] = len(dfa_states)
                    dfa_states.append(next_state)
                    if next_state & F:
                        dfa_final.add(next_state)

                    # Add to unprocessed states if it's a new state
                    unprocessed_states.append(next_state)

                # Add transition to DFA table (store state as frozenset)
                dfa[state_map[current_state]][symbol] = state_map[next_state]

    # Print only the state transitions in a readable format
    print("State Transitions:")
    for current_state in dfa_states:
        current_state_str = f"{{{' ,'.join(map(str, current_state))}}}"
        transitions = []
        for symbol in sigma:
            if symbol in dfa[state_map[current_state]]:
                next_state = dfa[state_map[current_state]][symbol]
                next_state_str = f"{{{' ,'.join(map(str, dfa_states[next_state]))}}}"
                transitions.append(f"{symbol} -> {next_state_str}")
        if transitions:
            print(f"  {current_state_str}: {', '.join(transitions)}")


def classify_grammar(grammar):
    vt, production = set(grammar["vt"]), grammar["production"]

    results = [
        (
            len(lhs) == 1 and lhs.isupper(), 
            list(map(lambda rhs: (
                all(symbol in vt or symbol.isupper() for symbol in rhs) and 
                (len(rhs) == 1 or (len(rhs) == 2 and rhs[1].isupper())),
                len(rhs) >= len(lhs)
            ), rhs_list))
        )
        for lhs, rhs_list in production.items()
    ]

    is_regular = all(lhs_ok and all(rhs_ok for rhs_ok, _ in rhs_checks) for lhs_ok, rhs_checks in results)

    is_context_free = all(lhs_ok for lhs_ok, _ in results)

    is_context_sensitive = all(all(sensitive_ok for _, sensitive_ok in rhs_checks) for _, rhs_checks in results)

    return ("Regular Grammar (Type 3)" if is_regular else
            "Context-Free Grammar (Type 2)" if is_context_free else
            "Context-Sensitive Grammar (Type 1)" if is_context_sensitive else
            "Recursively Enumerable Grammar (Type 0)")

if __name__ == "__main__":
    random.seed()
    config = load_config("config.json")
    
    print("Generated Strings:")
    for _ in range(5):
        print("Generated String:", generate_string(config["grammar"]))
    
    test_string = "abce"
    print(f'\nDoes string "{test_string}" belong to the language? {string_belongs_to_language(config["automaton"], test_string)}')
   
    print(classify_grammar(config["grammar"]))

    ndfa = (
        {'q0', 'q1', 'q2', 'q3'},  
        {'a', 'b', 'c'},
        {
            'q0': {'a': {'q0', 'q1'}},
            'q1': {'c': {'q1'}, 'b': {'q2'}},
            'q2': {'b': {'q3'}},
            'q3': {'a': {'q1'}}
        },  
        'q0', 
        {'q2'}  
    )

    dfa = ndfa_to_dfa(ndfa)
    print(dfa)
