package automaton

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
