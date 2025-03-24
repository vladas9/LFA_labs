class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nInitial State: {self.initial_state}\nFinal States: {self.final_states}"

class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

class NFAtoDFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.alphabet = list(nfa.alphabet)  # Alphabet of the NFA
        self.states = []  # List of DFA states (each state is a set of NFA states)
        self.transitions = {}  # DFA transitions
        self.final_states = set()  # DFA final states
        self.initial_state = None  # DFA initial state
        self.convert()  # Perform the conversion

    def convert(self):
        # Start with the initial state of the NFA and get its epsilon closure
        initial_dfa_state = self.epsilon_closure({self.nfa.initial_state})
        self.states.append(initial_dfa_state)
        self.initial_state = self.state_to_string(initial_dfa_state)

        unprocessed_states = [initial_dfa_state]

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            state_key = self.state_to_string(current_state)
            self.transitions[state_key] = {}

            for symbol in self.alphabet:
                next_state = self.epsilon_closure(self.move(current_state, symbol))
                if next_state:
                    next_state_key = self.state_to_string(next_state)

                    # If the next state is new, add it to the list of states
                    if not any(self.state_to_string(s) == next_state_key for s in self.states):
                        self.states.append(next_state)
                        unprocessed_states.append(next_state)

                    # Add the transition to the DFA
                    if symbol not in self.transitions[state_key]:
                        self.transitions[state_key][symbol] = []
                    self.transitions[state_key][symbol].append(next_state_key)

            # Check if the current state contains any NFA final states
            if any(state in self.nfa.final_states for state in current_state):
                self.final_states.add(state_key)

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        # Loop to calculate the epsilon closure
        while stack:
            state = stack.pop()
            if state in self.nfa.transitions:
                # Check if there is a transition for epsilon (empty string)
                if '' in self.nfa.transitions[state]:
                    for next_state in self.nfa.transitions[state]['']:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)

        return closure

    def move(self, states, symbol):
        result = set()
        # Loop over all states to get the set of reachable states on the given symbol
        for state in states:
            if state in self.nfa.transitions and symbol in self.nfa.transitions[state]:
                result.update(self.nfa.transitions[state][symbol])
        return result

    def state_to_string(self, state_set):
        return ','.join(sorted(state_set))

    def to_dfa(self):
        # Convert states to strings
        dfa_states = [self.state_to_string(state) for state in self.states]
        dfa_transitions = {}

        # Convert transitions to the DFA format
        for state_key, transitions in self.transitions.items():
            dfa_transitions[state_key] = {}
            for symbol, next_states in transitions.items():
                dfa_transitions[state_key][symbol] = next_states[0]

        # Return the final DFA
        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )

# Example NFA
nfa_states = {'q0', 'q1', 'q2', 'q3'}
alphabet = {'a', 'c', 'b'}
transitions = {
    'q0': {'a': {'q0', 'q1'}},
    'q1': {'c': {'q1'}, 'b': {'q2'}},
    'q2': {'b': {'q3'}},
    'q3': {'a': {'q1'}}
}
initial_state = 'q0'
final_states = {'q2'}

nfa = NFA(nfa_states, alphabet, transitions, initial_state, final_states)

# Convert NFA to DFA
converter = NFAtoDFAConverter(nfa)
dfa = converter.to_dfa()

# Print the DFA
print(dfa)
