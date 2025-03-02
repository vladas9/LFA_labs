import random
import json
from functools import reduce

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
