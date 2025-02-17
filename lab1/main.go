package main

import (
	"fmt"
	"lfa_labs/lab1/automaton"
	"lfa_labs/lab1/grammar"
	"math/rand"
	"time"
)

func main() {
	rand.New(rand.NewSource(time.Now().UnixNano()))

	grammarInstance := grammar.NewGrammar()

	for i := 0; i < 5; i++ {
		fmt.Println("Generated String:", grammarInstance.GenerateString())
	}

	automatonInstance := automaton.NewFiniteAutomaton()
	testString := "abce" // You can change this string to test different cases
	fmt.Printf("Does string \"%s\" belong to the language? %v\n", testString, automatonInstance.StringBelongToLanguage(testString))
}
