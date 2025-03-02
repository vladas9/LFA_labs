# Finite Automaton and Grammar Classification

## Task 1: Understanding Automaton and Its Uses

An **automaton** (plural: **automata**) is a mathematical model of computation that describes a system that can be in one of a finite number of states at any given time. It can transition between these states based on inputs, which are governed by a set of rules (often called a **transition function**). Automata are used to model systems that perform computations or follow predefined patterns, and they form the basis for many areas of computer science, such as formal languages, compilers, and automata theory.

### Types of Automata

1. **Finite Automata (FA)**: Used to recognize regular languages. Can be either **deterministic** (DFA) or **non-deterministic** (NFA). They have a finite set of states and can be used for applications like lexical analysis, text search, and simple pattern recognition.
2. **Pushdown Automata (PDA)**: Used for context-free languages, which can describe more complex structures, such as those used in programming languages' syntax.
3. **Turing Machines (TM)**: Used for recursively enumerable languages and represent a more general computational model capable of simulating any algorithm.

### Uses of Automata

- **Compiler Design**: Automata help recognize the structure of programming languages. For example, a regular grammar (using a finite automaton) can describe the syntax of simple tokens like identifiers, operators, and keywords.
- **Text Processing**: Automata are employed in string matching and pattern recognition algorithms.
- **Network Protocols**: Automata can model the state changes in communication protocols and validate correct protocol sequences.
- **Artificial Intelligence**: They are used in decision-making systems, where states represent different stages of problem-solving.

---

## Task 2: Classifying Grammar Based on Chomsky Hierarchy

The **Chomsky hierarchy** categorizes grammars into four types based on their generative power. The types, ordered from least to most powerful, are:

1. **Type 3 (Regular Grammar)**: Can be represented by finite automata. A regular grammar has production rules where the right-hand side of each rule is either a single terminal or a single terminal followed by a non-terminal. Example: \( A \rightarrow aB \).
2. **Type 2 (Context-Free Grammar)**: Can be represented by pushdown automata. A context-free grammar has production rules where the left-hand side of each rule is a single non-terminal. Example: \( S \rightarrow aSb \).
3. **Type 1 (Context-Sensitive Grammar)**: Requires a linear-bounded automaton for recognition. A context-sensitive grammar allows production rules where the length of the left-hand side is less than or equal to the length of the right-hand side. Example: \( A \rightarrow aB \).
4. **Type 0 (Recursively Enumerable Grammar)**: The most general grammar, which can be recognized by a Turing machine.

To classify a grammar based on the Chomsky hierarchy, we can analyze the structure of its production rules. Here's how we can determine the type of grammar:

- **Regular Grammar (Type 3)**: All productions are of the form \( A \rightarrow aB \) or \( A \rightarrow a \), where \( A \) is a non-terminal, and \( a \) is a terminal.
- **Context-Free Grammar (Type 2)**: All productions are of the form \( A \rightarrow \alpha \), where \( A \) is a non-terminal and \( \alpha \) can be a string of terminals and non-terminals.
- **Context-Sensitive Grammar (Type 1)**: All productions are of the form \( \alpha A \rightarrow \beta \), where the length of \( \alpha \) is less than or equal to the length of \( \beta \).
- **Recursively Enumerable Grammar (Type 0)**: If the grammar does not fit into any of the above categories, it is classified as recursively enumerable.

### Code Implementation for Grammar Classification:

```python
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
```
#### Explanation of the Code:

1. **Input**: The function takes a grammar in the form of a dictionary with keys:
    
    - `"vt"`: The set of terminal symbols.
    - `"production"`: A dictionary of production rules, where each key is a non-terminal and the value is a list of right-hand sides of the rules.
2. **Step-by-step check**:
    
    - **Regular Grammar Check**: The function checks if every production either has one terminal followed by a non-terminal or just a terminal.
    - **Context-Free Grammar Check**: It ensures that every left-hand side has only one non-terminal and checks the right-hand sides for validity.
    - **Context-Sensitive Grammar Check**: The function verifies if the length of the right-hand side is greater than or equal to the left-hand side.
    - **Recursively Enumerable Grammar Check**: If the grammar doesn't fit into any of the above categories, it is classified as Type 0.
3. **Output**: The function returns a string indicating the type of grammar based on the checks.


## Task 3: Converting a Finite Automaton to a Regular Grammar

### Given Variant 1:

The following information is provided for the finite automaton:

- \( Q = \{q_0, q_1, q_2, q_3\} \) — the set of states.
- \( \Sigma = \{a, c, b\} \) — the alphabet.
- \( F = \{q_2\} \) — the set of accepting states.
- The transition function \( \delta \) is as follows:
  - \( \delta(q_0, a) = q_0 \)
  - \( \delta(q_0, a) = q_1 \)
  - \( \delta(q_1, c) = q_1 \)
  - \( \delta(q_1, b) = q_2 \)
  - \( \delta(q_2, b) = q_3 \)
  - \( \delta(q_3, a) = q_1 \)

---

### Task a: Implement conversion of a finite automaton to a regular grammar

To convert a finite automaton (FA) to a regular grammar, we follow the general rule that each state in the FA corresponds to a non-terminal in the grammar. The transitions in the FA become production rules in the grammar.

1. **States Corresponding to Non-Terminals**: Each state \( q \in Q \) is mapped to a non-terminal symbol \( A_q \). So:
   - \( q_0 \) becomes \( A_{q_0} \)
   - \( q_1 \) becomes \( A_{q_1} \)
   - \( q_2 \) becomes \( A_{q_2} \)
   - \( q_3 \) becomes \( A_{q_3} \)

2. **Transition Function to Production Rules**: For each transition \( \delta(q, a) = p \), we add a rule in the form:
   \[
   A_q \rightarrow aA_p
   \]
   - \( \delta(q_0, a) = q_0 \) gives the production \( A_{q_0} \rightarrow aA_{q_0} \)
   - \( \delta(q_0, a) = q_1 \) gives the production \( A_{q_0} \rightarrow aA_{q_1} \)
   - \( \delta(q_1, c) = q_1 \) gives the production \( A_{q_1} \rightarrow cA_{q_1} \)
   - \( \delta(q_1, b) = q_2 \) gives the production \( A_{q_1} \rightarrow bA_{q_2} \)
   - \( \delta(q_2, b) = q_3 \) gives the production \( A_{q_2} \rightarrow bA_{q_3} \)
   - \( \delta(q_3, a) = q_1 \) gives the production \( A_{q_3} \rightarrow aA_{q_1} \)

3. **Final State Transitions**: If a state is an accepting state (in this case \( q_2 \)), the corresponding non-terminal will have a production rule that allows for termination of the string. So:
   - \( A_{q_2} \rightarrow \epsilon \) (where \( \epsilon \) is the empty string)

The regular grammar corresponding to the FA is:

\[
A_{q_0} \rightarrow aA_{q_0} \mid aA_{q_1}
\]
\[
A_{q_1} \rightarrow cA_{q_1} \mid bA_{q_2}
\]
\[
A_{q_2} \rightarrow bA_{q_3} \mid \epsilon
\]
\[
A_{q_3} \rightarrow aA_{q_1}
\]

---

### Task b: Determine whether the FA is deterministic or non-deterministic

A finite automaton is deterministic (DFA) if for every state \( q \) and input symbol \( a \), there is exactly one transition. In contrast, an automaton is non-deterministic (NDFA) if for some state \( q \) and input symbol \( a \), there are multiple transitions or no transitions at all.

Looking at the transitions:
- \( \delta(q_0, a) = q_0 \) and \( \delta(q_0, a) = q_1 \), which means there are two transitions for the symbol 'a' from state \( q_0 \).
- This violates the condition for determinism, so the FA is **non-deterministic**.

---

### Task c: Implement functionality to convert an NDFA to a DFA

To convert a Non-Deterministic Finite Automaton (NDFA) to a Deterministic Finite Automaton (DFA), we use the **subset construction (powerset construction)** algorithm. The basic steps are as follows:

1. **Start with the initial state of the NDFA**: Create a new DFA state that represents the set of NDFA states reachable from the NDFA's initial state. This is the initial state of the DFA.
   
2. **For each state in the DFA, consider all possible input symbols**: For each state in the DFA, compute the set of states that can be reached from the current DFA state on each input symbol. Each set of NDFA states forms a new DFA state.

3. **Repeat the process until no new states are discovered**.

4. **Accepting states**: Any DFA state that contains an NDFA accepting state is an accepting state in the DFA.

---

### Task d: Represent the FA graphically

To represent the FA graphically, we can use libraries such as `graphviz` or `networkx` in Python, or external tools like `AutomataLib`.

Here is an example of how you might represent this automaton graphically using Python and `graphviz`:

```python
from graphviz import Digraph

# Create a new directed graph
dot = Digraph()

# Add states as nodes
dot.node('q0', shape='circle')
dot.node('q1', shape='circle')
dot.node('q2', shape='doublecircle')  # Accepting state
dot.node('q3', shape='circle')

# Add transitions
dot.edge('q0', 'q0', label='a')
dot.edge('q0', 'q1', label='a')
dot.edge('q1', 'q1', label='c')
dot.edge('q1', 'q2', label='b')
dot.edge('q2', 'q3', label='b')
dot.edge('q3', 'q1', label='a')

# Render the graph to a file
dot.render('fa_graph', format='png', view=True)
