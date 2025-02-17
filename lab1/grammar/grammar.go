package grammar

import (
	"math/rand"
	"strings"
)

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
