# Implementation of Grammar and Finite Automaton

### Course: Formal Languages & Finite Automata

### Author: Amza Vladislav

---

## Theory

In formal language theory, a **grammar** defines a set of production rules used to generate strings from a given alphabet. The grammar consists of non-terminal symbols, terminal symbols, and production rules. A **finite automaton** is a computational model that accepts or rejects strings of symbols based on state transitions, using a set of states, an alphabet, a transition function, a start state, and a set of accepting states.

In this work, we implemented a **context-free grammar** (CFG) to generate strings and a **deterministic finite automaton**(DFA) to verify if a string belongs to a given language. The grammar and automaton are tied together to showcase the relationship between grammar and automaton theory.

## Objectives:

- To implement a context-free grammar that generates strings from a defined language.
- To implement a finite automaton that accepts or rejects strings based on state transitions.
- To combine the two components and verify whether generated strings belong to the language recognized by the finite automaton.

## Implementation description

### 1. Grammar Structure and Generation

The **grammar** is defined using the following components:

- **Non-terminal symbols (Vn)**: `{S, P, Q}`.
- **Terminal symbols (Vt)**: `{a, b, c, d, e, f}`.
- **Production rules**: Define how non-terminal symbols are replaced by other symbols. For example, the start symbol `S` can be replaced by either `aP` or `bQ`.
- **Start symbol**: `S`.

The grammar generates strings by recursively replacing non-terminal symbols with one of their production rules. The `GenerateString()` function generates strings starting from the start symbol `S`.
```go
type Grammar struct {
	Vn          map[string]struct{}
	Vt          map[string]struct{}
	Production  map[string][]string
	StartSymbol string
}

func NewGrammar() *Grammar {
	return &Grammar{
		Vn: map[string]struct{}{"S": {}, "P": {}, "Q": {}},
		Vt: map[string]struct{}{"a": {}, "b": {}, "c": {}, "d": {}, "e": {}, "f": {}},
		Production: map[string][]string{
			"S": {"aP", "bQ"},
			"P": {"bP", "cP", "dQ", "e"},
			"Q": {"eQ", "fQ", "a"},
		},
		StartSymbol: "S",
	}
}

func (g *Grammar) GenerateString() string {
	return g.generateFromNonTerminal(g.StartSymbol)
}

func (g *Grammar) generateFromNonTerminal(nonTerminal string) string {
	productions, exists := g.Production[nonTerminal]
	if !exists {
		return ""
	}

	production := productions[rand.Intn(len(productions))]
	var result strings.Builder

	for _, symbol := range production {
		if _, isTerminal := g.Vt[string(symbol)]; isTerminal {
			result.WriteString(string(symbol))
		} else {
			result.WriteString(g.generateFromNonTerminal(string(symbol)))
		}
	}

	return result.String()
}
```
This code defines the grammar and its generation function. It randomly selects one of the production rules and replaces non-terminal symbols recursively to generate valid strings.

### 2. Finite Automaton Structure

The **finite automaton** is defined by:

- **States**: `{q0, q1, q2, q3}`.
- **Input alphabet**: `{a, b, c, d, e, f}`.
- **Start state**: `q0`.
- **Accepting state**: `q3`.
- **Transition function**: Defines the state transitions based on the input symbols.

The automaton checks whether a given input string belongs to the language recognized by the automaton based on the transition rules.
```go
type FiniteAutomaton struct {
	Delta map[string]map[string]string
	q0    string
	F     map[string]struct{}
}

func NewFiniteAutomaton() *FiniteAutomaton {
	return &FiniteAutomaton{
		Delta: map[string]map[string]string{
			"q0": {"a": "q1", "b": "q2"},
			"q1": {"b": "q1", "c": "q1", "d": "q2", "e": "q3"},
			"q2": {"e": "q2", "f": "q2", "a": "q3"},
			"q3": {},
		},
		q0: "q0",
		F: map[string]struct{}{
			"q3": {},
		},
	}
}

func (fa *FiniteAutomaton) StringBelongToLanguage(inputString string) bool {
	currentState := fa.q0

	for _, symbol := range inputString {
		stateTransition, exists := fa.Delta[currentState][string(symbol)]
		if !exists {
			return false
		}
		currentState = stateTransition
	}

	_, isAcceptingState := fa.F[currentState]
	return isAcceptingState
}
```

The automaton's `StringBelongToLanguage()` function processes an input string character by character, following the transition rules, and checks if it ends in an accepting state (`q3`).

### 3. Main Application Logic

The main program generates strings using the grammar and tests them against the automaton. It calls the `GenerateString()` function from the grammar and checks if the generated string belongs to the language defined by the automaton using the `StringBelongToLanguage()` function.
```go
func main() {
	rand.New(rand.NewSource(time.Now().UnixNano()))

	grammarInstance := grammar.NewGrammar()

	for i := 0; i < 5; i++ {
		fmt.Println("Generated String:", grammarInstance.GenerateString())
	}

	automatonInstance := automaton.NewFiniteAutomaton()
	testString := "abce"
	fmt.Printf("Does string \"%s\" belong to the language? %v\n", testString, automatonInstance.StringBelongToLanguage(testString))
}

```

This code generates five random strings using the grammar and tests if a string belongs to the language defined by the finite automaton.
## Results
![image1](../images/lab1_ex1)
![image2](../images/lab1_ex2)
## Conclusions

The implementation successfully demonstrates the relationship between context-free grammar and finite automata. The grammar generates valid strings, and the finite automaton is able to verify whether the generated strings belong to the language it recognizes. The combination of these two components shows how formal languages can be both generated and recognized using automata.

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, M. (2006). _Introduction to Automata Theory, Languages, and Computation_(3rd ed.). Pearson.
2. Sipser, M. (2012). _Introduction to the Theory of Computation_ (3rd ed.). Cengage Learning.

4o mini
